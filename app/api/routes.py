from flask import Blueprint, request
from ..models import User, IncomeDeduction
from ..apiauthhelper import basic_auth, token_auth
api = Blueprint('api', __name__)





############# API LOGIN ROUTES  #############

@api.route('/api/signup', methods=["POST"])

def signUpPageAPI():
    data = request.json
   
       
    username = data['username']
    email = data['email']
    password = data['password']
    


    # add user to database
    user = User(username, email, password)

    user.saveToDB()

    return {
        'status': 'ok',
        'message': "Succesffuly created an account!"
    }

@api.route('/api/login', methods=["POST"])

@basic_auth.login_required
def getToken():
    user = basic_auth.current_user()
    if user is not None:
        return {
            'status': 'ok',
            'user': user.to_dict(),
        }
    else:
        return {
            'status': 'error',
            'message': 'Unauthorized Access'
        }, 401
    
############# API BUDGET ROUTE  #############
@api.route('/api/budget', methods=["POST"])
@token_auth.login_required
def updateBudget():
    data = request.json
    user = token_auth.current_user()

    # Get the user ID
    user_id = user.user_id

    # Update income and deductions for the user
    if 'paychecks' in data:
        for paycheck in data['paychecks']:
            income = IncomeDeduction(paycheck['title'], float(paycheck['amount']), 'income', paycheck['trans_date'], user_id)
            income.save()

    if 'bills' in data:
        for bill in data['bills']:
            deduction = IncomeDeduction(bill['title'], float(bill['amount']), 'deduction', bill['trans_date'], user_id)
            deduction.save()

    return {
        'status': 'ok',
        'message': 'Budget updated successfully'
    }

@api.route('/api/budget/remove', methods=["POST"])
@token_auth.login_required
def deleteEntry():
    data = request.json
    user = token_auth.current_user()

    # Get the user ID
    user_id = user.user_id

    # Delete income and deductions for the user
    if 'paychecks' in data:
        for paycheck in data['paychecks']:
            income = IncomeDeduction.query.filter_by(title=paycheck['title'], amount=float(paycheck['amount']), trans_date=paycheck['trans_date'], user_id=user_id).first()
            if income:
                income.delete()
                print(f"Paycheck '{paycheck['title']}' deleted for user '{user.username}'")
            else:
                print(f"No paycheck found with title '{paycheck['title']}' for user '{user.username}'")

    if 'bills' in data:
        for bill in data['bills']:
            deduction = IncomeDeduction.query.filter_by(title=bill['title'], amount=float(bill['amount']), trans_date=bill['trans_date'], user_id=user_id).first()
            if deduction:
                print('Deleting bill:', bill['title'])
                deduction.delete()
                print(f"Bill '{bill['title']}' deleted for user '{user.username}'")
            else:
                print(f"No bill found with title '{bill['title']}' for user '{user.username}'")

    return {
        'status': 'ok',
        'message': 'Budget updated successfully'
    }

@api.route('/api/budget/paychecks', methods=['GET'])
@token_auth.login_required
def get_paychecks():
    user = token_auth.current_user()
    user_id = user.user_id
    
    paychecks = IncomeDeduction.query.filter_by(category='income', user_id=user_id).all()
    
    paycheck_list = [paycheck.to_dict() for paycheck in paychecks]

    return {
        'status': 'ok',
        'paychecks': paycheck_list
    }

@api.route('/api/budget/bills', methods=['GET'])
@token_auth.login_required
def get_bills():
    user = token_auth.current_user()
    user_id = user.user_id
    
    bills = IncomeDeduction.query.filter_by(category='deduction', user_id=user_id).all()
    
    bill_list = [bill.to_dict() for bill in bills]

    return {
        'status': 'ok',
        'bills': bill_list
    }