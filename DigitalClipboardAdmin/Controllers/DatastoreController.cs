using DigitalClipboardAdmin.Models;
using Newtonsoft.Json;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Data;
using System.Data.OleDb;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Windows;

namespace DigitalClipboardAdmin.Controllers
{
    public class DatastoreController : BaseClass
    {
        private const string dcLogPath = "\\\\riemfs01\\X\\AutomationTools\\Digital_Clipboard_Logs\\";
        private const string dcLocalPath = "C:\\Users\\eric.hansen\\Desktop\\DC_Logs\\";

        private const string jsonPath = "\\\\riemfs01\\X\\AutomationTools\\Digital_Clipboard_Admin\\Database.json";
        private const string dbPath = "\\\\riemfs01\\S\\Research Support\\S-6 Information Management\\Administrative Tools\\Software\\DATABASE\\IMB_Software_DB_BackEnd.accdb";

        private static string conString = @"Provider=Microsoft.ACE.OLEDB.12.0;Data Source='S:\Research Support\S-6 Information Management\Administrative Tools\Software\DATABASE\IMB_Software_DB_BackEnd.accdb'";

        /// <summary>
        /// returns bools for each dependency object
        /// </summary>
        /// <returns>
        /// <para>dcLogsExist - does digital clipboard exist</para>
        /// <para>jsonExist - does does json db exist</para>
        /// <para>dbExist - does access db exist</para>
        /// </returns>
        public static (bool, bool, bool) CheckDependecies()
        {

            Log.Add("Init Data Sets");
            try
            {
                bool dcLogsExist;
                bool jsonExist = false;
                bool dbExist = false;

                // Log Files
                if (!Directory.Exists(dcLogPath))
                {
                    Log.Add("DC Log Dir Created");
                    Directory.CreateDirectory(dcLogPath);
                    dcLogsExist = true;
                }
                else
                {
                    dcLogsExist = true;
                }

                // JSON DB File
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
                else
                {
                    if (!File.Exists(jsonPath))
                    {
                        Log.Add("Json File Created");
                        File.Create(jsonPath);
                    }

                    if (new FileInfo(jsonPath).Length > 0)
                        jsonExist = true;
                }

                // Access DB File
                if (!Directory.Exists(Path.GetDirectoryName(dbPath)))
                {
                    Log.Add("DB Path Doesn't Exist");
                }else if (!File.Exists(dbPath))
                {
                    Log.Add("DB File Doesn't Exist");
                }
                else
                {
                    dbExist = true;
                }

                return (dcLogsExist, jsonExist, dbExist);
            }catch(Exception e)
            {
                Log.Add("Error: " + e.Message, Log.Level.ERR);
                return (false, false, false);
            }
        }

        public static JsonStorageModel GetJsonDB()
        {
            Log.Add("GetJsonDB");
            try
            {
                string jsonStr = "";
                using (StreamReader reader = new StreamReader(jsonPath))
                {
                    jsonStr = reader.ReadToEnd();
                }

                // Deserialize DB
                return JsonConvert.DeserializeObject<JsonStorageModel>(jsonStr);
            }catch(Exception e)
            {
                Log.Add("GetJsonDB Error: " + e.Message, Log.Level.ERR);
                return null;
            }
        }

        public static bool SetJsonDB(JsonStorageModel jsm)
        {
            Log.Add("SetJsonDB");
            string jsmStr = JsonConvert.SerializeObject(jsm);
            try
            {
                using(StreamWriter writer = new StreamWriter(jsonPath))
                {
                    writer.Write(jsmStr);
                    writer.Flush();
                }
                Log.Add("Write Complete");
                return true;
                // Set DC Logs to Processed
                // TODO:

            }catch(Exception e)
            {
                Log.Add("SetJsonDB Error: " + e.Message, Log.Level.ERR);
                return false;
            }
        }

        public static List<string> GetDCLogs()
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

        public static void SetDCLogs()
        {
            try
            {
                Log.Add("SetDCLogs");
                DirectoryInfo dir = new DirectoryInfo(dcLogPath);
                FileInfo[] files = dir.GetFiles("*.log", SearchOption.TopDirectoryOnly);

                foreach (FileInfo item in files)
                {
                    TimeSpan ts = DateTime.Now.Subtract(item.CreationTime);

                    if (ts.TotalDays > 7)
                    {
                        string name = item.FullName.Replace(".log", ".plog");
                        if (!item.FullName.Contains(".plog"))
                            File.Move(item.FullName, name);
                    }
                }

            }
            catch (Exception e)
            {
                Log.Add("SetDCLogs Error:" + e.Message, Log.Level.ERR);
            }
        }

        public static Dictionary<string, List<EntryModel>> ConvertDCLogs(List<string> lines = null)
        {
            if (lines == null)
                lines = GetDCLogs();

            Log.Add("ConvertDCLogs");
            Dictionary<string, List<EntryModel>> convEntries = new Dictionary<string, List<EntryModel>>();

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

                    if (convEntries.ContainsKey(em.ECN))
                    {
                        convEntries[em.ECN].Add(em);
                    }
                    else
                    {
                        convEntries.Add(em.ECN, new List<EntryModel>() { em });
                    }
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
            Software,
            SoftwareLicense,
            SoftwareMap
        }
        private static string[] Queries = new string[]
        {
            "Select * from tblComputers;",
            "Select * from tblUsers;",
            "Select * from tblHRH;",
            "Select * from tblSoftware;",
            "Select * from tblSoftwareLicenses;",
            "Select * from tblSoftwareInUse;"
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
   
        public static Dictionary<string, DeviceModel> ConvertToDevice(IEnumerable<List<object>> lst = null)
        {
            Log.Add("ConvertToDevice");
            if (lst == null)
                lst = GetDbQuery(QueryType.Device);

            Dictionary<string, DeviceModel> devices = new Dictionary<string, DeviceModel>();

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
                    Notes = (item as List<object>)[10].ToString(),
                    Make = (item as List<object>)[11].ToString(),
                    Model = (item as List<object>)[12].ToString(),
                    ModelNumber = (item as List<object>)[13].ToString(),
                    HRH_ID = (item as List<object>)[14].ToString()
                };
                if (devices.ContainsKey(dm.Name))
                {
                    devices[dm.Name] = dm;
                    MessageBox.Show("Duplicate " + dm.Name);
                    Log.Add("Duplicate DeviceModel " + dm.Name);
                }
                else
                {
                    devices.Add(dm.Name, dm);
                }
            }

            return devices;
        }

        public static Dictionary<string, UserModel> ConvertToUser(IEnumerable<List<object>> lst = null)
        {
            Log.Add("ConvertToUser");
            if (lst == null)
                lst = GetDbQuery(QueryType.User);

            Dictionary<string, UserModel> users = new Dictionary<string, UserModel>();

            foreach (object item in lst)
            {
                UserModel um = new UserModel()
                {
                    UserID = (item as List<object>)[0].ToString(),
                    FirstName = (item as List<object>)[1].ToString(),
                    LastName = (item as List<object>)[2].ToString()
                };
                if (users.ContainsKey(um.UserID))
                {
                    users[um.UserID] = um;
                    MessageBox.Show("Duplicate " + um.UserID);
                    Log.Add("Duplicate UserModel " + um.UserID);
                }
                else
                {
                    users.Add(um.UserID, um);
                }
            }

            return users;
        }

        public static Dictionary<string, HRHModel> ConvertToHRH(IEnumerable<List<object>> lst = null)
        {
            Log.Add("ConvertToUser");
            if (lst == null)
                lst = GetDbQuery(QueryType.HRH);

            Dictionary<string, HRHModel> HRH = new Dictionary<string, HRHModel>();

            foreach (object item in lst)
            {
                HRHModel um = new HRHModel()
                {
                    HolderID = (item as List<object>)[0].ToString(),
                    FirstName = (item as List<object>)[1].ToString(),
                    LastName = (item as List<object>)[2].ToString()
                };
                if (HRH.ContainsKey(um.HolderID))
                {
                    HRH[um.HolderID] = um;
                    MessageBox.Show("Duplicate " + um.HolderID);
                    Log.Add("Duplicate HRHModel " + um.HolderID);
                }
                else
                {
                    HRH.Add(um.HolderID, um);
                }
            }

            return HRH;
        }

        public static (Dictionary<string, MappedModel>, Dictionary<string, List<EntryModel>>) CreateMapping
            (Dictionary<string, List<EntryModel>> entries, Dictionary<string, DeviceModel> devices)
        {
            Log.Add("CreateMapping");
            Dictionary<string, MappedModel> mappings = new Dictionary<string, MappedModel>();
            Dictionary<string, List<EntryModel>> nonMapped = new Dictionary<string, List<EntryModel>>();

            // Check Null
            if(devices == null || devices.Count == 0)
                return (null, null);
            
            // Loop through all devices and map entries by ecn
            foreach (KeyValuePair<string, DeviceModel> device in devices)
            {
                if (entries.ContainsKey(device.Value.ECN))
                {
                    MappedModel mm = new MappedModel()
                    {
                        DeviceModelID = device.Key,
                        Barcode = EntryModel.GetBarcode(entries[device.Value.ECN]),
                        ECN = device.Value.ECN
                    };
                    mappings.Add(mm.ECN, mm);
                }
            }

            // Any ecn that doesn't get mapped
            foreach (var entry in entries)
            {
                if (!mappings.ContainsKey(entry.Key))
                {
                    nonMapped.Add(entry.Key, entry.Value);
                }
            }

            return (mappings, nonMapped);
        }
    }
        
}
