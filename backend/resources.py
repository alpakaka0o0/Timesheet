from flask_restx import Resource, Namespace
from flask import Flask, jsonify, request
import sys
from models import db, Employee, Timesheet, Timecheck
from datetime import datetime
from flask import Response
import json

payroll_ns = Namespace('payroll', description='Payroll Overview Page API 목록')
    
# 업데이트된 임금 정보를 받음 
@payroll_ns.route('/payroll')
class PayrollInfoAPI(Resource):
    def get(self):
        data = [
            {
                "month": 8,
                "data": [
                    {
                        "employee": "Somi",
                        "totalHours": 55,
                        "salary": 5500
                    }
                ]
            },
           {
                "month": 7,
                "data": [
                {
                    "employee": "Jiwon",
                    "totalHours": 60,
                    "salary": 6000
                },
                {
                    "employee": "Somi",
                    "totalHours": 55,
                    "salary": 5500
                }
                ]
            },
            {
                "month": 6,
                "data": [
                {
                    "employee": "Somi",
                    "totalHours": 60,
                    "salary": 5000
                },
                {
                    "employee": "Jiwon",
                    "totalHours": 60,
                    "salary": 6000
                }
                ]
            } 
        ]
        return data;
 
#2. uploadImage page
upload_ns = Namespace('upload', description='Upload Image Pgae API 목록')

#타임시트지 이미지 전송
@upload_ns.route('/timesheet-image')
class TimesheetImageAPI(Resource):
    @payroll_ns.doc('get_payroll_info')
    def post(self):
    	return {"hello" : "restx"}
    
 
#3. modifyInfo page
modi_ns = Namespace('modify', description='Modify Info Page API 목록')

#ocr 결과 받음
@modi_ns.route('/ocr-result')
class OcrResultAPI(Resource):
    @modi_ns.doc('get_ocr_result',
                 description='OCR 처리된 결과를 가져옵니다.', 
                 responses={200: '성공', 400: '요청 오류'})
    def get(self):
    	return {"hello" : "restx"}

#편집된 타임시트지 전송
@modi_ns.route('/timesheet-edit')
class ModiAPI(Resource):
    @modi_ns.doc('save_timesheet_edit')
    def post(self):
        json_data = request.get_json()
        print('Json data: ', json_data)
        employee_name = json_data['name']
        print('employee name: ', employee_name)

        # Employee 검색
        employee = Employee.query.filter_by(first_name=employee_name).first()
        if not employee:
            print('!!!!No name!!!!')
            return jsonify({"message": "Employee not found"}), 404
        else: 
            print("!!!!yes name")
            
        # Timesheet 생성 및 저장
        timesheet = Timesheet(
            employee_id=employee.id,
            week_starting_date=datetime.utcnow(),
            pay_per_hour=int(json_data['ratePerHour']),
            over_time_pay=int(json_data['overtimePay']),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(timesheet)
        db.session.commit()  # Timesheet 커밋

        # Timecheck 생성 및 저장
        for entry in json_data['data']:
            date = datetime.strptime(entry['date'], '%m/%d/%Y')
            in_time = datetime.strptime(entry['timeIn'], '%H:%M').time()
            out_time = datetime.strptime(entry['timeOut'], '%H:%M').time()
            timecheck = Timecheck(
                timesheet_id=timesheet.id,
                date=datetime.combine(date, datetime.min.time()),
                in_time=datetime.combine(date, in_time),
                out_time=datetime.combine(date, out_time),
                late_entry=False,
                early_exit=False,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(timecheck)

        db.session.commit()
        # 응답 객체 생성
        response_data = {"message": "Timesheet data saved successfully"}
        print("Response data:", response_data)  # 콘솔에 출력하여 확인
        return Response(
            response=json.dumps(response_data),
            status=200,
            mimetype='application/json'
        )
        #return jsonify({"message": "Timesheet data saved successfully"}), 200
            