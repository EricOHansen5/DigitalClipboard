using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DigitalClipboardAdmin.Shared
{
    public static class Constants
    {
        public static string CheckedIn = "Checked In";
        public static string CheckedOut = "Checked Out";

        public static string CheckIn = "Check In";
        public static string CheckOut = "Check Out";

        public static string CheckInStr = "--IN --";
        public static string CheckOutStr = "--OUT--";
        public static string EmptyTechStr = "No Technician";

        public static string dcLogPath = "\\\\riemfs01\\X\\AutomationTools\\Digital_Clipboard_Logs\\";
        public static string dcLocalPath = "C:\\Users\\eric.hansen\\Desktop\\DC_Logs\\";

        public static string jsonPath = "\\\\riemfs01\\X\\AutomationTools\\Digital_Clipboard_Admin\\Database.json";
        public static string dbPath = "\\\\riemfs01\\S\\Research Support\\S-6 Information Management\\Administrative Tools\\Software\\DATABASE\\IMB_Software_DB_BackEnd.accdb";

        public static string conString = @"Provider=Microsoft.ACE.OLEDB.12.0;Data Source='S:\Research Support\S-6 Information Management\Administrative Tools\Software\DATABASE\IMB_Software_DB_BackEnd.accdb'";
    }
}
