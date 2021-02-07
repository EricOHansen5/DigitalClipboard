using DigitalClipboardAdmin.Controllers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace DigitalClipboardAdmin.Models
{
    public class DeviceModel : BaseClass
    {

        private string _UserID;
        public string UserID
        {
            get { return _UserID; }
            set { if (value != _UserID) _UserID = value; OnPropertyChanged(); }
        }

        // Unique ID
        private string _Name;
        public string Name
        {
            get { return _Name; }
            set {
                if (value != _Name)
                {
                    _Name = value;
                    ECN = ParseECN(_Name);
                }
                    OnPropertyChanged(); }
        }


        private string _ECN;
        public string ECN
        {
            get { return _ECN; }
            set { if (value != _ECN) _ECN = value; OnPropertyChanged(); }
        }

        public static string ParseECN(string name)
        {
            // Parse Name for ECN
            return Regex.Match(name, @"\d+").Value;
        }
        
        private string _Division;
        public string Division
        {
            get { return _Division; }
            set { if (value != _Division) _Division = value; OnPropertyChanged(); }
        }
        private string _IP;
        public string IP
        {
            get { return _IP; }
            set { if (value != _IP) _IP = value; OnPropertyChanged(); }
        }
        private string _MAC;
        public string MAC
        {
            get { return _MAC; }
            set { if (value != _MAC) _MAC = value; OnPropertyChanged(); }
        }
        private string _MAC_Wireless;
        public string MAC_Wireless
        {
            get { return _MAC_Wireless; }
            set { if (value != _MAC_Wireless) _MAC_Wireless = value; OnPropertyChanged(); }
        }
        private string _ServiceTag;
        public string ServiceTag
        {
            get { return _ServiceTag; }
            set { if (value != _ServiceTag) _ServiceTag = value; OnPropertyChanged(); }
        }
        private string _Network;
        public string Network
        {
            get { return _Network; }
            set { if (value != _Network) _Network = value; OnPropertyChanged(); }
        }
        private string _OS;
        public string OS
        {
            get { return _OS; }
            set { if (value != _OS) _OS = value; OnPropertyChanged(); }
        }
        private string _BIOS;
        public string BIOS
        {
            get { return _BIOS; }
            set { if (value != _BIOS) _BIOS = value; OnPropertyChanged(); }
        }

        private List<string> _Notes;
        public List<string> Notes
        {
            get { return _Notes; }
            set { if (value != _Notes) _Notes = value; OnPropertyChanged(); }
        }

        private string _Make;
        public string Make
        {
            get { return _Make; }
            set { if (value != _Make) _Make = value; OnPropertyChanged(); }
        }

        private string _Model;
        public string Model
        {
            get { return _Model; }
            set { if (value != _Model) _Model = value; OnPropertyChanged(); }
        }

        private string _ModelNumber;
        public string ModelNumber
        {
            get { return _ModelNumber; }
            set { if (value != _ModelNumber) _ModelNumber = value; OnPropertyChanged(); }
        }

        private string _HRH_ID;
        public string HRH_ID
        {
            get { return _HRH_ID; }
            set { if (value != _HRH_ID) _HRH_ID = value; OnPropertyChanged(); }
        }
    }
}
