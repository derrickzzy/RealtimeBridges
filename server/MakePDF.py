# generate PDF
import logging
logging.getLogger('xhtml2pdf').addHandler(logging.NullHandler())

def pdf(obj,msg_condition,DI):
    import jinja2
    import datetime
    from xhtml2pdf import pisa
    time = datetime.datetime.now().strftime("%Y/%m/%d-%H:%M")
    Environment = jinja2.Environment
    FileSystemLoader=jinja2.FileSystemLoader
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("templates/report.html")
    template_vars = {"title" : "Real-time Bridge Structural Health Monitoring",
                     "date": time,
                     "bname": obj.name,
                     "bnum": obj.number,
                     "bloc": obj.town+', '+obj.state,
                     "yearbuilt": obj.year,
                     "insepctiondate": obj.inspection,
                     "bcondition": msg_condition,
                     "bDI": DI
    }

    html_out = template.render(template_vars)

    resultFile = open('C:/Users/zzhao01/Documents/Webserver/website/Report.pdf', "w+b")
    pisa.CreatePDF(html_out.encode(), resultFile)
    resultFile.close()

if __name__ == '__main__':
    pdf(msg_condition,DI)
