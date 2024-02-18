from flask import Flask, render_template, request
from models import db, User, CategorySection, Category, TransLog
from sqlalchemy import exists, func
from flask import jsonify
from flask_cors import CORS
from enum import Enum
from datetime import datetime, timedelta

# create the extension
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

with app.app_context():
    try:
        print("Creating tables...")
        db.create_all()
        print("Tables created.")
    except Exception as e:
        print(f"Error creating tables: {e}")

CORS(app)

@app.route("/categoryListGet", methods=["POST"])
def categoryListGet():
    result = []
    typeValue = request.json.get('type')
    try:
        typeValue = int(typeValue)
    except ValueError:
        return jsonify({"error": "Invalid type value"}), 400

    categorySectionList = db.session.query(CategorySection).filter_by(type=typeValue).all()
    for category_section in categorySectionList:
        # section_data = {
        #     "value": category_section.id,
        #     "label": category_section.sectionName,
        #     "option": []
        # }
        section_data = {
            "id": category_section.id,
            "sectionName": category_section.sectionName,
            "option": []
        }
        category_options = db.session.query(Category).filter_by(sectionId=category_section.id).all()
        for category_option in category_options:
            # option_data = {
            #     "value": category_option.id,
            #     "label": category_option.categoryName
            # }
            option_data = {
                "id": category_option.id,
                "categoryName": category_option.categoryName
            }
            section_data["option"].append(option_data)

        result.append(section_data)

    print(result)
    return jsonify(result)


@app.route("/categorySectionSet", methods=["POST"])
def categorySectionSet():
    sectionType = request.json.get('type')
    sectionId = request.json.get('id')
    sectionName = request.json.get('sectionName')

    try:
        sectionId = int(sectionId)
    except ValueError:
        return jsonify({"error": "Invalid section ID"}), 400

    sameNameSection = db.session.query(CategorySection).filter_by(sectionName=sectionName,type=sectionType).first()
    if sameNameSection is not None:
        return jsonify({"error": "Section already exists"}), 400

    # remove id
    section_data = request.json.copy()
    section_data.pop('id', None)
    try:
        section = CategorySection(**section_data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if sectionId == 0:
        # New section
        db.session.add(section)
    else:
        # Existing section
        exist_section = CategorySection.query.get(sectionId)
        if exist_section is None:
            return jsonify({"error": "Section not found"}), 404
        exist_section.sectionName = section.sectionName
        exist_section.type = section.type
        exist_section.modifyTime = datetime.now()

    db.session.commit()
    return jsonify({"message": "Success"})


@app.route("/categorySectionDelete", methods=["POST"])
def categorySectionDelete():
    sectionId = request.json.get('id')

    try:
        sectionId = int(sectionId)
    except ValueError:
        return jsonify({"error": "Invalid section ID"}), 400

    section = db.session.query(CategorySection).get(sectionId)
    if section is None:
        return jsonify({"error": "Section not found"}), 404

    # categories = db.session.query(Category.id).filter_by(sectionId=sectionId).all()
    # category_ids = [category_id for (category_id,) in categories]

    # exists_criteria = db.session.query(exists().where(TransLog.categoryId.in_(category_ids))).scalar()
    # if exists_criteria:
    #     return jsonify({"error": "Cannot delete section with associated transactions"}), 400

    #Delete associated categories
    # db.session.query(Category).filter(Category.id.in_(categories)).delete(synchronize_session=False)

    db.session.flush()
    # Delete the section
    db.session.delete(section)
    db.session.commit()

    return jsonify({"message": "Success"})

@app.route("/categorySet", methods=["POST"])
def categorySet():
    categoryId = request.json.get('id')
    categoryName = request.json.get('categoryName')
    sectionId = request.json.get('sectionId')

    try:
        categoryId = int(categoryId)
    except ValueError:
        return jsonify({"error": "Invalid category ID"}), 400

    sameCategory = db.session.query(Category).filter_by(categoryName=categoryName,sectionId=sectionId).first()
    if sameCategory is not None:
        return jsonify({"error": "Category already exists"}), 400

    # remove id
    category_data = request.json.copy()
    category_data.pop('id', None)

    try:
        category = Category(**category_data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if categoryId == 0:
        # New category
        db.session.add(category)
    else:
        # Existing category
        existing_category = Category.query.get(categoryId)
        if existing_category is None:
            return jsonify({"error": "Category not found"}), 404
        existing_category.sectionId = category.sectionId
        existing_category.categoryName = category.categoryName
        existing_category.modifyTime = datetime.now()

    db.session.commit()
    return jsonify({"message": "Success"})


@app.route("/categoryDelete", methods=["POST"])
def categoryDelete():
    categoryId = request.json.get('id')

    try:
        categoryId = int(categoryId)
    except ValueError:
        return jsonify({"error": "Invalid category ID"}), 400

    category = Category.query.get(categoryId)
    if category is None:
        return jsonify({"error": "Category not found"}), 404

    exists_criteria = db.session.query(exists().where(TransLog.categoryId == categoryId)).scalar()
    if exists_criteria:
        return jsonify({"error": "Cannot delete category with associated transactions"}), 400

    db.session.delete(category)
    db.session.commit()

    return jsonify({"message": "Success"})

@app.route("/transLogsGet", methods=["POST"])
def TransLogsGet():
    startDate = request.json.get('startDate')
    endDate = request.json.get('endDate')
    if startDate is None or endDate is None:
        return jsonify({"error": "Invalid startDate or endDate"}), 400
    try:
        startDate = datetime.strptime(request.json.get('startDate'), '%Y-%m-%d %H:%M:%S.%f')
    except ValueError:
        return jsonify({"error": "Invalid startDate"}), 400

    try:
        endDate = datetime.strptime(request.json.get('endDate'), '%Y-%m-%d %H:%M:%S.%f')
    except ValueError:
        return jsonify({"error": "Invalid endDate"}), 400
    transLogList = db.session.query(TransLog, Category.categoryName, CategorySection.sectionName, CategorySection.type) \
        .join(Category, TransLog.categoryId == Category.id) \
        .join(CategorySection, Category.sectionId == CategorySection.id) \
        .filter((TransLog.transDate >= startDate) & (TransLog.transDate < endDate)).all()
    result = [
        {
            "id": log.TransLog.id,
            "transDate": log.TransLog.transDate.strftime('%Y-%m-%d %H:%M:%S.%f'),
            "categoryId": log.TransLog.categoryId,
            "amount": log.TransLog.amount,
            "memo": log.TransLog.memo,
            "categoryName": log.categoryName,
            "categorySectionName": log.sectionName,
            "type": log.type
        }
        for log in transLogList
    ]
    return jsonify(result)

@app.route("/transLogSet", methods=["POST"])
def transLogSet():
    transLogId = request.json.get('id')
    try:
        transLogId = int(transLogId)
    except ValueError:
        return jsonify({"error": "Invalid transLog ID"}), 400

    # remove id
    transLog_data = request.json.copy()
    transLog_data.pop('id', None)

    try:
        transLog = TransLog(**transLog_data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if transLogId == 0:
         # New transLog
        db.session.add(transLog)
    else:
         # Existing transLog
        existing_transLog = TransLog.query.get(transLogId)
        if existing_transLog is None:
            return jsonify({"error": "TransLog not found"}), 404
        existing_transLog.transDate = transLog.transDate
        existing_transLog.amount = transLog.amount
        existing_transLog.categoryId = transLog.categoryId
        existing_transLog.memo = transLog.memo
    db.session.commit()
    return jsonify({"message": "Success"})

@app.route("/transLogDelete", methods=["POST"])
def transLogDelete():
    transLogId = request.json.get('id')
    try:
        transLogId = int(transLogId)
    except ValueError:
        return jsonify({"error": "Invalid transLog ID"}), 400

    transLog = TransLog.query.get(transLogId)
    if transLog is None:
        return jsonify({"error": "TransLog not found"}), 404

    db.session.delete(transLog)
    db.session.commit()
    return jsonify({"message": "Success"})

@app.route("/monthReportGet", methods=["POST"])
def monthReportGet():
    date = request.json.get('date')
    if date is None:
        return jsonify({"error": "Invalid startDate or endDate"}), 400
    try:
        today = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
        startDate = datetime(today.year, today.month, 1)
        next_month = startDate.replace(day=1) + timedelta(days=32)
        endDate = next_month.replace(day=1)
    except ValueError:
        return jsonify({"error": "Invalid startDate"}), 400
    expenseAmount = db.session.query(func.sum(TransLog.amount)) \
        .join(Category, TransLog.categoryId == Category.id) \
        .join(CategorySection, Category.sectionId == CategorySection.id) \
        .group_by(CategorySection.sectionName) \
        .filter((TransLog.transDate >= startDate) & (TransLog.transDate < endDate) & (CategorySection.type == 1 )).all()

    expenseAmount_value = int(expenseAmount[0][0]) if expenseAmount and expenseAmount[0] and expenseAmount[0][0] else 0

    incomeAmount = db.session.query(func.sum(TransLog.amount)) \
        .join(Category, TransLog.categoryId == Category.id) \
        .join(CategorySection, Category.sectionId == CategorySection.id) \
        .group_by(CategorySection.sectionName) \
        .filter((TransLog.transDate >= startDate) & (TransLog.transDate < endDate) & (CategorySection.type == 0 )).all()

    incomeAmount_value = int(incomeAmount[0][0]) if incomeAmount and incomeAmount[0] and incomeAmount[0][0] else 0

    reportData = [{
        "expenseAmount": expenseAmount_value,
        "incomeAmount": incomeAmount_value,
        "balanceAmount": incomeAmount_value - expenseAmount_value
    }]
    return jsonify(reportData)


@app.route("/monthReportChartGet", methods=["POST"])
def MonthReportChartGet():
    date = request.json.get('date')
    type = request.json.get('type')
    if date is None:
        return jsonify({"error": "Invalid startDate or endDate"}), 400
    try:
        today = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
        startDate = datetime(today.year, today.month, 1)
        next_month = startDate.replace(day=1) + timedelta(days=32)
        endDate = next_month.replace(day=1)
    except ValueError:
        return jsonify({"error": "Invalid startDate"}), 400
    transLogList = db.session.query(CategorySection.sectionName,func.sum(TransLog.amount).label('total_amount')) \
        .join(Category, TransLog.categoryId == Category.id) \
        .join(CategorySection, Category.sectionId == CategorySection.id) \
        .group_by(CategorySection.sectionName) \
        .filter((TransLog.transDate >= startDate) & (TransLog.transDate < endDate) & (CategorySection.type == type)).all()

    #print(transLogList)

    chartData = {
        "labels": [item[0] for item in transLogList],
        "datasets": []
    }
    dataSet = {
        "data":[item[1] for item in transLogList],
    }
    chartData["datasets"].append(dataSet)

    #print(chartData)
    return jsonify(chartData)


@app.route("/initial")
def initial():
    initial_section = [
            {"name": "Active Income", "type": 0},
    {"name": "Passive Income", "type": 0},
    {"name": "Other", "type": 0},
    {"name": "Food", "type": 1},
    {"name": "Clothing", "type": 1},
    {"name": "Housing", "type": 1},
    {"name": "Transportation", "type": 1},
    {"name": "Education", "type": 1},
    {"name": "Entertainment", "type": 1},
    {"name": "Giving", "type": 1},
    {"name": "Other", "type": 1}
        # {"name": "主動", "type": 0},
        # {"name": "不勞而獲", "type": 0},
        # {"name": "其他", "type": 0},
        # {"name": "食", "type": 1},
        # {"name": "衣", "type": 1},
        # {"name": "住", "type": 1},
        # {"name": "行", "type": 1},
        # {"name": "育", "type": 1},
        # {"name": "樂", "type": 1},
        # {"name": "給予", "type": 1},
        # {"name": "其他", "type": 1}
    ]

    for data in initial_section:
        new_category_section = CategorySection(sectionName=data["name"], type=data["type"])
        db.session.add(new_category_section)
        db.session.commit()

    initial_category = [
          {"categoryName": "Salary", "sectionId": 1},
    {"categoryName": "Bonus", "sectionId": 1},
    {"categoryName": "Passive Income", "sectionId": 2},
    {"categoryName": "Lottery Winnings", "sectionId": 2},
    {"categoryName": "Subsidy", "sectionId": 3},
    {"categoryName": "Parental Support", "sectionId": 3},
    {"categoryName": "Dining Out", "sectionId": 4},
    {"categoryName": "Beverages", "sectionId": 4},
    {"categoryName": "Clothing", "sectionId": 5},
    {"categoryName": "Daily Essentials", "sectionId": 6},
    {"categoryName": "Transportation", "sectionId": 7},
    {"categoryName": "Self-Investment", "sectionId": 8},
    {"categoryName": "Entertainment", "sectionId": 9},
    {"categoryName": "Travel", "sectionId": 9},
    {"categoryName": "Gifts", "sectionId": 10},
    {"categoryName": "Parental Surprises", "sectionId": 10},
    {"categoryName": "Advance Payment", "sectionId": 10},
    {"categoryName": "Stop Loss", "sectionId": 11},
    {"categoryName": "Tax Payment", "sectionId": 11},
    {"categoryName": "Phone Bill", "sectionId": 11},
    {"categoryName": "Medical Expenses", "sectionId": 11}
        # {"categoryName": "薪資", "sectionId": 1},
        # {"categoryName": "獎金", "sectionId": 1},
        # {"categoryName": "被動收入", "sectionId": 2},
        # {"categoryName": "中獎回饋", "sectionId": 2},
        # {"categoryName": "補助", "sectionId": 3},
        # {"categoryName": "爸媽給", "sectionId": 3},
        # {"categoryName": "外食", "sectionId": 4},
        # {"categoryName": "飲料", "sectionId": 4},
        # {"categoryName": "服飾", "sectionId": 5},
        # {"categoryName": "日用品", "sectionId": 6},
        # {"categoryName": "交通", "sectionId": 7},
        # {"categoryName": "投資自己", "sectionId": 8},
        # {"categoryName": "娛樂", "sectionId": 9},
        # {"categoryName": "旅行", "sectionId": 9},
        # {"categoryName": "禮物", "sectionId": 10},
        # {"categoryName": "給爸媽", "sectionId": 10},
        # {"categoryName": "代墊", "sectionId": 10},
        # {"categoryName": "停損", "sectionId": 11},
        # {"categoryName": "繳稅", "sectionId": 11},
        # {"categoryName": "電話費", "sectionId": 11},
        # {"categoryName": "醫療", "sectionId": 11}
    ]

    for data in initial_category:
        new_category = Category(categoryName=data["categoryName"], sectionId=data["sectionId"])
        db.session.add(new_category)
        db.session.commit()


    return jsonify({"message": "Success"})

if __name__ == "__main__":
    app.run(debug=True)
