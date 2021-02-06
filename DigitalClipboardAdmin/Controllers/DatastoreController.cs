using DigitalClipboardAdmin.Models;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Data;
using System.Data.OleDb;
using System.Globalization;
using System.IO;
using System.Linq;

namespace DigitalClipboardAdmin.Controllers
{
    public class DatastoreController : BaseClass
    {
        private const string dcLogPath = "\\\\riemfs01\\X\\AutomationTools\\Digital_Clipboard_Logs\\";
        private const string dcLocalPath = "C:\\Users\\eric.hansen\\Desktop\\DC_Logs\\";

        private const string jsonPath = "\\\\riemfs01\\X\\AutomationTools\\Digital_Clipboard_Admin\\Database.json";
        private const string dbPath = "\\\\riemfs01\\S\\Research Support\\S-6 Information Management\\Administrative Tools\\Software\\DATABASE\\IMB_Software_DB_BackEnd.accdb";

        private bool dbPathExist = true;
        private static string conString = @"Provider=Microsoft.ACE.OLEDB.12.0;Data Source='S:\Research Support\S-6 Information Management\Administrative Tools\Software\DATABASE\IMB_Software_DB_BackEnd.accdb'";
        public DatastoreController()
        {
            Log.Add("Init Data Sets");
            try
            {
                if (!Directory.Exists(dcLogPath))
                {
                    Log.Add("DC Log Dir Created");
                    Directory.CreateDirectory(dcLogPath);
                }

                if (!Directory.Exists(Path.GetDirectoryName(jsonPath)))
                {
                    Log.Add("Json Dir Created");
                    Directory.CreateDirectory(Path.GetDirectoryName(jsonPath));
                    if (!File.Exists(jsonPath))
                    {
                        Log.Add("Json File Created");
                        File.Create(jsonPath);
                    }
                }

                if (!Directory.Exists(Path.GetDirectoryName(dbPath)))
                {
                    Log.Add("DB Path Doesn't Exist");
                    dbPathExist = false;
                }else if (!File.Exists(dbPath))
                {
                    Log.Add("DB File Doesn't Exist");
                    dbPathExist = false;
                }
            }catch(Exception e)
            {
                Log.Add("Error: " + e.Message, Log.Level.ERR);
            }
        }    

        public static List<string> ReadDCLogs()
        {
            try
            {
                Log.Add("ReadDCLogs");
                DirectoryInfo dir = new DirectoryInfo(dcLogPath);
                FileInfo[] files = dir.GetFiles("*.log", SearchOption.TopDirectoryOnly);

                List<string> final = new List<string>();

                foreach (FileInfo item in files)
                {
                    using(StreamReader sr = new StreamReader(item.FullName))
                    {
                        var lines = sr.ReadToEnd().Split('\n');
                        final.AddRange(lines);
                    }    
                }
                Log.Add("ReadDCLogs Complete, " + final.Count + " lines read.");
                return final;

            }catch(Exception e)
            {
                Log.Add("ReadDCLogs Error:" + e.Message, Log.Level.ERR);
                return null;
            }
        }

        public static List<EntryModel> ConvertDCLogs(List<string> lines)
        {
            Log.Add("ConvertDCLogs");
            List<EntryModel> convEntries = new List<EntryModel>();

            foreach (string line in lines)
            {
                string[] props = line.Replace("[", "").Replace("]","").Split(new char[] { '\t' }, StringSplitOptions.RemoveEmptyEntries);
                if(props.Length == EntryModel.PropertyCount)
                {
                    string[] dts = props[0].Split(new char[] {'_', '-', ':', '.' });
                    int[] dti = new int[6];
                    for (int i = 0; i < dts.Length; i++){ dti[i] = int.Parse(dts[i]); };
                    DateTime dt = new DateTime(dti[0], dti[1], dti[2], dti[3], dti[4], dti[5]);
                    EntryModel em = new EntryModel()
                    {
                        dateTime = dt,
                        checkIn = props[1] == EntryModel.CheckInStr ? true : false,
                        barcode = props[2],
                        ECN = props[3],
                        firstName = props[4].Split(' ').Length > 1 ? props[4].Split(' ')[0] : props[4],
                        lastName = props[4].Split(' ').Length > 1 ? props[4].Split(' ')[1] : "",
                        techName = props[5].Trim('\r')
                    };
                    convEntries.Add(em);
                }
            }
            Log.Add("ConvertDCLogs Complete, converted " + convEntries.Count + ".");
            return convEntries;
        }
    
        private static OleDbConnection GetDbConnection()
        {
            try
            {
                Log.Add("GetDbConnection");
                return new OleDbConnection(conString);
            }catch(Exception e)
            {
                Log.Add("DB Connection Error: " + e.Message, Log.Level.ERR);
                return null;
            }
        }

        public enum QueryType
        {
            Device,
            User,
            HRH,
            Software
        }
        private static string[] Queries = new string[]
        {
            "Select * from tblComputers;",
            "Select * from tblUsers;",
            "Select * from tblHRH;",
            "Select * from tblSoftware;"
        };
        public static IEnumerable<List<object>> GetDbQuery(QueryType qt)
        {
            Log.Add("GetDbQuery");
            List<object> lst = new List<object>();
            OleDbConnection con = GetDbConnection();
            OleDbCommand command = new OleDbCommand(Queries[(int)qt], con);

            con.Open();
            using (OleDbDataReader reader = command.ExecuteReader())
            {
                var ix = Enumerable.Range(0, reader.FieldCount).ToList();
                foreach (IDataRecord record in reader as IEnumerable)
                    yield return ix.Select(i => record[i]).ToList();
            }
            con.Close();
            Log.Add("GetDbQuery Complete");
        }
   
        public static List<DeviceModel> ConvertToDevice(IEnumerable<List<object>> lst)
        {
            List<DeviceModel> devices = new List<DeviceModel>();

            foreach (object item in lst)
            {
                DeviceModel dm = new DeviceModel()
                {
                    Name = (item as List<object>)[0].ToString(),
                    UserID = (item as List<object>)[1].ToString(),
                    BIOS = (item as List<object>)[2].ToString(),
                    Division = (item as List<object>)[3].ToString(),
                    IP = (item as List<object>)[4].ToString(),
                    MAC = (item as List<object>)[5].ToString(),
                    MAC_Wireless = (item as List<object>)[6].ToString(),
                    ServiceTag = (item as List<object>)[7].ToString(),
                    Network = (item as List<object>)[8].ToString(),
                    OS = (item as List<object>)[9].ToString(),
                    Notes = new List<string>() { (item as List<object>)[10].ToString() },
                    Make = (item as List<object>)[11].ToString(),
                    Model = (item as List<object>)[12].ToString(),
                    ModelNumber = (item as List<object>)[13].ToString(),
                    HRH_ID = (item as List<object>)[14].ToString()
                };
                devices.Add(dm);
            }

            return devices;
        }
    }
        
}
