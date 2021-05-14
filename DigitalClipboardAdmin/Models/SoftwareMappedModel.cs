using DigitalClipboardAdmin.Controllers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DigitalClipboardAdmin.Models
{
    public class SoftwareMappedModel:BaseClass
    {
        // Unique
        private string _UseID;
        public string UseID
        {
            get { return _UseID; }
            set { if (value != _UseID) _UseID = value; OnPropertyChanged(); }
        }

        // DeviceModel.Name
        private string _DeviceName;
        public string DeviceName
        {
            get { return _DeviceName; }
            set { if (value != _DeviceName) _DeviceName = value; OnPropertyChanged(); }
        }

        // SoftwareLicense.LicenseID
        private string _LicenseID;
        public string LicenseID
        {
            get { return _LicenseID; }
            set { if (value != _LicenseID) _LicenseID = value; OnPropertyChanged(); }
        }

    }
}
