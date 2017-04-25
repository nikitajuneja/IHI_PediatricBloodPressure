import web

urls = (
    "/bprangechecker/checkrange", "/bprangecheckercard"
)

rangeChecker = RangeChecker()

class bprangechecker:
    def GET(self):
        data=web.input()
        height=int(data.height)
        age=int(data.age)
        gender=int(data.gender)
        systolic=int(data.systolic)
        diastolic=int(data.diastolic)
        fromRangeChecker = rangeChecker.check_bp(height, age, gender, systolic, diastolic)
        return fromRangeChecker


class bprangecheckercard:
    def GET(self):
        data=web.input()
        bpstatus=int(data.bpstatus)
        cards = rangeChecker.getCards(bpstatus)






