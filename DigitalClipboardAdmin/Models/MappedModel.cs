using DigitalClipboardAdmin.Controllers;
using System.Collections.Generic;

namespace DigitalClipboardAdmin.Models
{
    public class MappedModel:BaseClass
    {
        // ECN
        private string _DeviceModelID;
        public string DeviceModelID
        {
            get { return _DeviceModelID; }
            set { if (value != _DeviceModelID) _DeviceModelID = value; OnPropertyChanged(); }
        }

        private DeviceModel _DeviceModel;
        public DeviceModel DeviceModel
        {
            get { return _DeviceModel; }
            set { if (value != _DeviceModel) _DeviceModel = value; OnPropertyChanged(); }
        }

        private List<EntryModel> _Entries = new List<EntryModel>();
        public List<EntryModel> Entries
        {
            get { return _Entries; }
            set { if (value != _Entries) _Entries = value; OnPropertyChanged(); }
        }

    }
}
