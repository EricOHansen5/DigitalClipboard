using DigitalClipboardAdmin.Controllers;
using System;
using System.Collections.Generic;

namespace DigitalClipboardAdmin.Models
{
    public class MappedModel:BaseClass
    {
        // Name
        private string _DeviceModelID;
        public string DeviceModelID
        {
            get { return _DeviceModelID; }
            set { if (value != _DeviceModelID) _DeviceModelID = value; OnPropertyChanged(); }
        }

        private string _Barcode;
        public string Barcode
        {
            get { return _Barcode; }
            set { if (value != _Barcode) _Barcode = value; OnPropertyChanged(); }
        }

        private string _ECN;
        public string ECN
        {
            get { return _ECN; }
            set { if (value != _ECN) _ECN = value; OnPropertyChanged(); }
        }

        private string _Name;
        public string Name
        {
            get { return _Name; }
            set { if (value != _Name) _Name = value; OnPropertyChanged(); }
        }
    }
}
