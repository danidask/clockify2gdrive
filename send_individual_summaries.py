import settings
from clockify import get_reports_summary
import operator


def get_engineers_registers(month, year):
    projects, engineers, registers = get_reports_summary(month, year)
    engineers_registers = {}
    for register in registers:
        project = register[0]
        username = register[1]
        duration = register[2]
        description = register[3]
        date = register[4]
        if username not in engineers_registers:
            engineers_registers[username] = []
        engineers_registers[username].append((project, username, duration, description, date))  # username is not needed but to keek the format
    return engineers_registers


def generate_user_report_for_telegram(engineer_registers):
    report = ""
    duration_total = 0
    projects = set()
    for register in engineer_registers:
        project = register[0]
        # username = register[1]
        duration = register[2]
        description = register[3]
        date = register[4]
        month_day_str =  date.strftime("%m/%d")  # 07/21
        report += "{}\t{}\t'{}'\t{}h\n".format(month_day_str, project, description, duration)
        duration_total += duration
        projects.add(project)
    report += "Total {} hours in {} registers for {} projects".format(duration_total, len(engineer_registers),
                                                                      len(projects))
    return report


def telegram_send_user_report(report, tg_id):
    # TODO
    print(report)


if __name__ == '__main__':
    engineers_registers = get_engineers_registers(7, 2019)

    for engineer in engineers_registers.keys():
        # print(engineer)  # Jhon Doe
        engineer_registers = engineers_registers[engineer]
        # print(engineer_registers)  # list of tuples
        tg_id = settings.telegram_users.get(engineer)
        if tg_id is None:
            print("User '{}' does not have telegram id, so no report will be sent".format(engineer))
        else:
            engineer_registers.sort(key=operator.itemgetter(4), reverse=False)  # sort for date
            report = generate_user_report_for_telegram(engineer_registers)
            telegram_send_user_report(report, tg_id)
