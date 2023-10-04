"""define result"""
from datetime import datetime, timedelta


def date_week(day_month):
    """find date in begin week for answer"""
    year = datetime.now().year
    date = str(year) + "-"
    months = [
        "января",
        "февраля",
        "марта",
        "апреля",
        "мая",
        "июня",
        "июля",
        "августa",
        "сентября",
        "октября",
        "ноября",
        "декабря",
    ]
    for i, month in enumerate(months):
        if month == day_month.split(" ")[1]:
            date = date + str(i + 1) + "-" + str(day_month.split(" ")[0])
            date = datetime.strptime(date, "%Y-%m-%d")
            break
    return str(date)


def format_time(time, date_title):
    """make a standard response time"""
    time_format = datetime.strptime(time, "%H:%M")
    time_change = date_title + timedelta(
        hours=time_format.hour, minutes=time_format.minute
    )
    time_str = time_change.strftime("%Y-%m-%dT%H:%M:%S")
    return time_str


def common_time(b_t, e_t, b_s, e_s):  # begin_teacher....end_student
    """find common time between two people"""
    teacher = datetime.strptime(b_t, "%H:%M")
    student = datetime.strptime(b_s, "%H:%M")
    begin_common_time = max(teacher, student)
    teacher = datetime.strptime(e_t, "%H:%M")
    student = datetime.strptime(e_s, "%H:%M")
    end_common_time = min(teacher, student)
    if end_common_time - begin_common_time >= timedelta(hours=1, minutes=45):
        res = (
            begin_common_time.strftime("%H:%M")
            + "-"
            + end_common_time.strftime("%H:%M")
        )
        return res
    return ""


def change_begin_time(begin):
    """add change"""
    if begin == datetime.strptime("09:30", "%H:%M"):
        begin = begin + timedelta(hours=0, minutes=0)
    elif begin == datetime.strptime("12:50", "%H:%M"):
        begin = begin + timedelta(hours=0, minutes=50)
    elif begin == datetime.strptime("15:15", "%H:%M"):
        begin = begin + timedelta(hours=0, minutes=10)
    elif begin == datetime.strptime("17:55", "%H:%M"):
        begin = begin + timedelta(hours=0, minutes=5)
    elif begin == datetime.strptime("18:45", "%H:%M"):
        begin = begin + timedelta(hours=0, minutes=15)
    elif begin == datetime.strptime("18:55", "%H:%M"):
        begin = begin + timedelta(hours=0, minutes=5)
    else:
        begin = begin + timedelta(hours=0, minutes=10)
    return begin


def change_end_time(end):
    """subtract change"""
    if end == datetime.strptime("11:15", "%H:%M"):
        end = end - timedelta(hours=0, minutes=10)
    elif end == datetime.strptime("13:40", "%H:%M"):
        end = end - timedelta(hours=0, minutes=50)
    elif end == datetime.strptime("15:25", "%H:%M"):
        end = end - timedelta(hours=0, minutes=10)
    elif end == datetime.strptime("17:10", "%H:%M"):
        end = end - timedelta(hours=0, minutes=10)
    elif end == datetime.strptime("20:40", "%H:%M"):
        end = end - timedelta(hours=0, minutes=5)
    else:
        end = end - timedelta(hours=0, minutes=5)
    return end


def break_time(result_time):
    """divide time into 2 parts"""
    res = ["", ""]
    result_time = result_time.split("-")
    begin = datetime.strptime(result_time[0], "%H:%M")
    begin_new = change_begin_time(begin)
    end = datetime.strptime(result_time[1], "%H:%M")
    end_new = change_end_time(end)
    if end_new - begin_new >= timedelta(hours=1, minutes=35):
        res[0] = begin_new.strftime("%H:%M")
        res[1] = end_new.strftime("%H:%M")
    return res


class FreeTimeManager:
    def __init__(self):
        self.free_time_dict = {}
        self.timetable_unchanged_list = []
        self.answer_list = []
        self.place_university = "Университетский проспект"
        self.flag = "False"
        self.timetable = {"student": {}, "teacher": {}}

    def add_json_free_time(self, day, begin, end, places, person, num):
        """string add in free time file"""
        one_str = {
            "day": day.split(", ")[0],
            "day_month": day.split(", ")[1],
            "time_begin": end,
            "place_begin": places[0],
            "time_end": begin,
            "place_end": places[1],
        }
        self.free_time_dict[person][num].append(one_str)

    def add_json_answer(self, day_month, time_begin, time_end, color, title):
        """string add in response array"""
        date = date_week(day_month)
        date_title = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        if title == "":
            title = date_title.strftime("%d.%m.%Y")
        time_begin_str = format_time(time_begin, date_title)
        time_end_str = format_time(time_end, date_title)
        one_str = {
            "title": title,
            "start": time_begin_str,
            "end": time_end_str,
            "color": color,
        }
        self.answer_list.append(one_str)

    def add_json_unchanged(
        self,
        day_month,
        type_subject,
        subject,
        place,
        time_begin,
        time_end,
        color,
        title,
    ):
        """string add in response array"""
        date = date_week(day_month)
        date_title = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        if title == "":
            title = date_title.strftime("%d.%m.%Y")
        time_begin_str = format_time(time_begin, date_title)
        time_end_str = format_time(time_end, date_title)
        full_place = place.split(",")
        if len(full_place) > 1:
            cab = full_place[len(full_place) - 1].strip()
            title = title + ", " + type_subject + ", каб. " + cab
        else:
            title = title + ", " + type_subject
        one_str = {
            "title": title,
            "start": time_begin_str,
            "end": time_end_str,
            "color": color,
            "subject": subject,
            "place": place,
        }
        self.timetable_unchanged_list.append(one_str)

    def free_time(self):
        """free time for person"""
        for person in self.timetable:
            for num in self.timetable[person]:
                self.free_time_dict[person][num] = []
                for day in self.timetable[person][num]:
                    prev = None
                    end = "09:30"
                    for i in self.timetable[person][num][day]:
                        begin = i["time_begin"]
                        # end first lesson, begin second lesson
                        if prev is not None and prev["time_begin"] == i["time_begin"]:
                            if prev["time_end"] > i["time_end"]:
                                i["time_end"] = prev["time_end"]
                        elif prev is not None and prev["time_end"] == i["time_end"]:
                            if prev["time_begin"] <= i["time_begin"]:
                                i["time_begin"] = prev["time_begin"]
                            else:
                                self.free_time_dict[person][num].pop()
                        self.estimate_time(end, begin, day, person, num)
                        end = i["time_end"]
                        prev = i.copy()
                    self.estimate_time(end, "20:40", day, person, num)

    def estimate_time(self, end_time, begin_time, day, person, num):
        """check if the time is fits"""
        end = datetime.strptime(end_time, "%H:%M")
        begin = datetime.strptime(begin_time, "%H:%M")
        if begin - end >= timedelta(hours=1, minutes=45):
            if self.flag == "True":
                places = ["", ""]
                self.add_json_free_time(day, begin_time, end_time, places, person, num)
            else:
                places = self.check_place(end_time, begin_time, day, person, num)
                if places[0] == places[1]:
                    self.add_json_free_time(
                        day, begin_time, end_time, places, person, num
                    )
                else:
                    if begin - end >= timedelta(hours=3, minutes=45):
                        self.add_json_free_time(
                            day, begin_time, end_time, places, person, num
                        )

    def check_place(
        self, end, begin, day, person, num
    ):  # end first lesson, begin second lesson
        """check location match"""
        place = ["", ""]
        for i in self.timetable[person][num][day]:
            if end == i["time_end"]:
                place[0] = i["place"]
            if begin == i["time_begin"]:
                place[1] = i["place"]
            if begin == "20:40":
                place[1] = self.place_university
            if end == "09:30":
                place[0] = self.place_university
        return place

    def change_json_free_time(self, day, time_begin, time_end, person, key):
        """change free time array"""
        one_str = {
            "day_month": day,
            "time_begin": time_begin,
            "place_begin": self.place_university,
            "time_end": time_end,
            "place_end": self.place_university,
        }
        self.free_time_dict[person][key].append(one_str)

    def check_common_time_persons(self, flag):
        """check common time teacher(student) and teacher(student)"""
        for _, person_i in enumerate(self.free_time_dict):
            keys = self.free_time_dict[person_i].keys()
            key_list = []
            for k in keys:
                key_list.append(k)
            for p in range(len(key_list) - 1):
                person1_dict = self.free_time_dict[person_i][key_list[p]]
                person2_dict = self.free_time_dict[person_i][key_list[p + 1]]

                self.free_time_dict[person_i].pop(key_list[p])
                self.free_time_dict[person_i].pop(key_list[p + 1])

                self.free_time_dict[person_i][key_list[p + 1]] = []
                person2_dict_last = person2_dict.copy()
                for person1 in person1_dict:
                    day_check = False
                    for person2 in person2_dict:
                        if person1["day_month"] == person2["day_month"]:
                            day_check = True
                            result_time = self.compare_place(person1, person2, flag)
                            if result_time != "":
                                time_b, time_e = break_time(result_time)
                                if time_b != time_e:
                                    time_begin, time_end = result_time.split("-")
                                    self.change_json_free_time(
                                        person1["day_month"],
                                        time_begin,
                                        time_end,
                                        person_i,
                                        key_list[p + 1],
                                    )

    def free_time_in_answer(self):
        """make response a free time file"""
        color_list = [
            "#71AB7E",
            "#ffcc99",
            "#E3DD95",
            "#6D6D6e",
            "#F1B7B3",
            "#B8A8CC",
            "#99ccff",
            "#73d978",
            "#ccff66",
        ]
        color_number = 0
        count = len(self.free_time_dict["student"]) + len(
            self.free_time_dict["teacher"]
        )
        for i in self.free_time_dict:
            color_number += 1
            for j in self.free_time_dict[i]:
                for k in self.free_time_dict[i][j]:
                    if count == 1:
                        color = "#4e8bb1"
                    else:
                        color = color_list[color_number % 9]
                    self.add_json_answer(
                        k["day_month"],
                        k["time_begin"],
                        k["time_end"],
                        color,
                        "",
                    )

    def break_time_in_dict(self):
        """change break time"""
        for i in self.free_time_dict:
            for k in self.free_time_dict[i]:
                for j in self.free_time_dict[i][k]:
                    j["time_begin"], j["time_end"] = break_time(
                        j["time_begin"] + "-" + j["time_end"]
                    )

    def find_common_time(self):
        """find common time depending on the situation"""
        len_teacher, len_student = len(self.free_time_dict["teacher"]), len(
            self.free_time_dict["student"]
        )
        if len_teacher == len_student == 1:
            self.check_common_time_s_t(self.flag, True)
        elif (len_teacher > 0 and len_student == 0) or (
            len_student > 0 and len_teacher == 0
        ):
            self.check_common_time_persons(self.flag)
            self.break_time_in_dict()
            self.free_time_in_answer()
        elif len_teacher > 0 and len_student > 0:
            self.check_common_time_persons(self.flag)
            self.check_common_time_s_t(self.flag, False)

    def check_common_time_s_t(self, flag, with_day_check):
        """check common time student and teacher"""
        color = "#4e8bb1"
        for k1 in self.free_time_dict["teacher"]:
            for i in self.free_time_dict["teacher"][k1]:
                day_check = False
                for k2 in self.free_time_dict["student"]:
                    for j in self.free_time_dict["student"][k2]:
                        if j["day_month"] == i["day_month"]:
                            day_check = True
                            result_time = self.compare_place(i, j, flag)
                            if result_time != "":
                                time_begin, time_end = break_time(result_time)
                                if time_begin != time_end:
                                    self.add_json_answer(
                                        i["day_month"],
                                        time_begin,
                                        time_end,
                                        color,
                                        "",
                                    )
                if not day_check and with_day_check:
                    result_time = common_time(
                        i["time_begin"], i["time_end"], "09:30", "20:40"
                    )
                    if result_time != "":
                        time_begin, time_end = break_time(result_time)
                        if time_begin != time_end:
                            self.add_json_answer(
                                i["day_month"], time_begin, time_end, color, ""
                            )

    def compare_place(self, person1, person2, flag):
        if flag == "False":
            b_1, e_1 = self.change_time(person1)
            b_2, e_2 = self.change_time(person2)
            return common_time(b_1, e_1, b_2, e_2)
        else:
            return common_time(
                person1["time_begin"],
                person1["time_end"],
                person2["time_begin"],
                person2["time_end"],
            )

    def change_time(self, person):
        begin = datetime.strptime(person["time_begin"], "%H:%M")
        end = datetime.strptime(person["time_end"], "%H:%M")
        if person["place_begin"] != self.place_university:
            begin = begin + timedelta(hours=2, minutes=0)
        if person["place_end"] != self.place_university:
            end = end - timedelta(hours=2, minutes=0)
        return begin.strftime("%H:%M"), end.strftime("%H:%M")

    def timetable_unchanged(self):
        """add in answer array with color"""
        global timetable
        color_list = [
            "#71AB7E",
            "#ffcc99",
            "#E3DD95",
            "#6D6D6e",
            "#F1B7B3",
            "#B8A8CC",
            "#99ccff",
            "#73d978",
            "#ccff66",
        ]
        color_number = 0
        for person in self.timetable:
            for num in self.timetable[person]:
                color_number += 1
                for i in self.timetable[person][num]:
                    for j in self.timetable[person][num][i]:
                        color = color_list[color_number % 9]
                        self.add_json_unchanged(
                            i.split(", ")[1],
                            j["type_subject"],
                            j["subject"],
                            j["full_place"],
                            j["time_begin"],
                            j["time_end"],
                            color,
                            num,
                        )

        self.delete_repeat()

    def delete_repeat(self):
        """delete repeat in answer"""
        i = 1
        while i <= len(self.timetable_unchanged_list) - 1:
            answer1, answer2 = (
                self.timetable_unchanged_list[i].copy(),
                self.timetable_unchanged_list[i - 1].copy(),
            )
            title1, title2 = answer1["title"].split(",", 2), answer2["title"].split(
                ",", 2
            )
            place1, place2 = answer1["place"].split(",", 1), answer2["place"].split(
                ",", 1
            )
            places = "," + place1[len(place1) - 1] + ",\n" + place2[len(place2) - 1]
            cabs = "," + title1[len(title1) - 1] + "," + title2[len(title2) - 1]

            answer1["title"], answer2["title"] = ",".join(title2[:2]), ",".join(
                title2[:2]
            )
            answer1["place"], answer2["place"] = ",".join(place1[:1]), ",".join(
                place2[:1]
            )

            if self.timetable_unchanged_list[i] == self.timetable_unchanged_list[i - 1]:
                self.timetable_unchanged_list.pop(i)
            elif answer1 == answer2:
                answer1["title"] = answer1["title"] + cabs
                answer1["place"] = answer1["place"] + places
                self.timetable_unchanged_list[i - 1] = answer1
                self.timetable_unchanged_list.pop(i)

            else:
                i += 1

    def main(self, flag, timetable_val):
        """define result"""
        self.timetable = timetable_val
        self.flag = flag
        self.free_time_dict = {"teacher": {}, "student": {}}
        self.answer_list, self.timetable_unchanged_list = [], []

        self.timetable_unchanged()
        self.free_time()
        self.find_common_time()
