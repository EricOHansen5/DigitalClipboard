using DigitalClipboardAdmin.Controllers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DigitalClipboardAdmin.Models
{
    public class SoftwareLicenseModel:BaseClass
    {
        // SoftwareMappedModel.LicenseID
        private string _LicenseID;
        public string LicenseID
        {
            get { return _LicenseID; }
            set { if (value != _LicenseID) _LicenseID = value; OnPropertyChanged(); }
        }
        
        // SoftwareModel.ID
        private string _SoftwareID;
        public string SoftwareID
        {
            get { return _SoftwareID; }
            set { if (value != _SoftwareID) _SoftwareID = value; OnPropertyChanged(); }
        }
        
        private string _Version;
        public string Version
        {
            get { return _Version; }
            set { if (value != _Version) _Version = value; OnPropertyChanged(); }
        }
        
        private string _SN;
        public string SN
        {
            get { return _SN; }
            set { if (value != _SN) _SN = value; OnPropertyChanged(); }
        }
        
        private int _Owned;
        public int Owned
        {
            get { return _Owned; }
            set { if (value != _Owned) _Owned = value; OnPropertyChanged(); }
        }
        
        private int _Upgrade;
        public int Upgrade
        {
            get { return _Upgrade; }
            set { if (value != _Upgrade) _Upgrade = value; OnPropertyChanged(); }
        }
        
        private int _Available;
        public int Available
        {
            get { return _Available; }
            set { if (value != _Available) _Available = value; OnPropertyChanged(); }
        }
        
        private string _Notes;
        public string Notes
        {
            get { return _Notes; }
            set { if (value != _Notes) _Notes = value; OnPropertyChanged(); }
        }
        
        private string _Division;
        public string Division
        {
            get { return _Division; }
            set { if (value != _Division) _Division = value; OnPropertyChanged(); }
        }
    }
}
