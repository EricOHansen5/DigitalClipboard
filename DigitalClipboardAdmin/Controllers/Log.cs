using System;
using System.IO;
using System.Linq;

namespace DigitalClipboardAdmin.Controllers
{
    public static class Log
    {
        public static string dir = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
        public static string filename = dir + "/DigitalClipboard/logs.txt";
        public static string GEN = "  GENERAL   ";
        public static string WARN = "--WARNING-- ";
        public static string ERR = "!  ERROR   !";
        public static string CRIT = "!!CRITICAL!!";
        public enum Level
        {
            GEN,
            WARN,
            ERR,
            CRIT
        }
        public static string[] Levels = new string[] { GEN, WARN, ERR, CRIT };

        public static StreamWriter Writer { get; set; }

        public static void Add(string message, Level level = Level.GEN)
        {
            try
            {
                if (!File.Exists(filename))
                    Directory.CreateDirectory(Path.GetDirectoryName(filename));

                Writer = new StreamWriter(filename, true);

                Writer.WriteLine(string.Format("{0} : {1} : {2}", DateTime.Now, Levels[(int)level], message));
                Writer.Flush();

                if(level == Level.ERR)
                {
                    Send_Logs();
                }
            }
            catch (Exception e)
            {
                BaseClass.EShow("ERROR WRITING LOG: " + e.Message);
                throw;
            }
            finally
            {
                Writer.Close();
                Writer.Dispose();
            }
        }

        public static void Clear_Log()
        {
            FileInfo fi = new FileInfo(filename);
            if (fi.Length > 200000)
            {
                var lines = File.ReadAllLines(filename);
                File.WriteAllLines(filename, lines.Skip(lines.Length / 2).ToArray());
            }
        }

        public static void Send_Logs()
        {
            try
            {
                string logdir = @"\\riemfs01\x\AutomationTools\Digital_Clipboard_Admin_Logs";
                string name = DateTime.Now.ToString("(yyyy.MM.dd.HH.mm)_") + Environment.UserName + ".txt";
                File.Copy(filename, Path.Combine(logdir, name), true);
                BaseClass.Show("Logs Sent!");
            }
            catch (Exception ex)
            {
                Add("Unable to copy log to X:\\AutomationTools\\Digital_Clipboard_Admin_Logs : " + ex.Message);
            }
        }

    }
}
