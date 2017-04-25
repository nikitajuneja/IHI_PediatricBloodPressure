import json

# assuming age in years, height in cms, gender as M or F, BP readings in mmHg
def check_bp(height, age, gender, systolic, diastolic):

    normalSystolicPressureLower=0
    normalSystolicPressureHigher=0
    normalDiastolicPressureLower=0
    normalDiastolicPressureHigher=0
    bpstatus = 'normal'

    if age>=0 and age<1:
        normalSystolicPressureLower=75
        normalSystolicPressureHigher=100
        normalDiastolicPressureLower=50
        normalDiastolicPressureHigher=70
    elif age>=1 and age<5:
        normalSystolicPressureLower=80
        normalSystolicPressureHigher=110
        normalDiastolicPressureLower=50
        normalDiastolicPressureHigher=80
    elif age>=5 and age<13:
        normalSystolicPressureLower=85
        normalSystolicPressureHigher=120
        normalDiastolicPressureLower=55
        normalDiastolicPressureHigher=80
    elif age>=13 and age<=18:
        normalSystolicPressureLower=95
        normalSystolicPressureHigher=140
        normalDiastolicPressureLower=60
        normalDiastolicPressureHigher=90


    if systolic<normalSystolicPressureLower:
        bpstatus='low'
    elif  systolic>normalSystolicPressureHigher:
        bpstatus = 'high'
    else:
        bpstatus = 'normal'

    data = {}
    data['normalSystolicPressureLower'] = normalSystolicPressureLower
    data['normalSystolicPressureHigher'] = normalSystolicPressureHigher
    data['normalDiastolicPressureLower'] = normalDiastolicPressureLower
    data['normalDiastolicPressureHigher'] = normalDiastolicPressureHigher
    data['bpstatus'] = bpstatus
    json_data = json.dumps(data)

    return json_data


def getCards(bpstatus):
    card1 = ''
    card2 = ''
    card3 = ''

    if bpstatus == 'low':
        card1 = 'LowBPGuideline1'
        card2 = 'LowBPGuideline2'
        card3 = 'LowBPGuideline3'
    elif bpstatus == 'high':
        card1 = 'HighBPGuideline1'
        card2 = 'HighBPGuideline2'
        card3 = 'HighBPGuideline3'

    data = {}
    data['card1'] = card1
    data['card2'] = card2
    data['card3'] = card3
    json_data = json.dumps(data)

    return json_data
