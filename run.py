import http.server
import socketserver
import cgi
import gspread
from google.oauth2 import service_account

# Google Sheets API setup
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = service_account.Credentials.from_service_account_file("creds.json", scopes=scope)
client = gspread.authorize(creds)

# Open the spreadsheet
spreadsheet = client.open("info_log")

# Access the worksheet by its name
worksheet = spreadsheet.worksheet("info_log")

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/submit':
            ctype, pdict = cgi.parse_header(self.headers['content-type'])
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                name = fields.get('name')[0].decode('utf-8')
                amount = fields.get('amount')[0].decode('utf-8')
                date = fields.get('date')[0].decode('utf-8')
                type_ = fields.get('type')[0].decode('utf-8')
                on_bill = fields.get('on_bill')[0].decode('utf-8')

                # Append data to Google Sheet
                worksheet.append_row([name, amount, date, type_, on_bill])

                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()

httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()
