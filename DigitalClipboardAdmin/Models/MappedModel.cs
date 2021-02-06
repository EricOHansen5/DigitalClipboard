using DigitalClipboardAdmin.Controllers;

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

        // ECN
        private string _EntryModelID;
        public string EntryModelID
        {
            get { return _EntryModelID; }
            set { if (value != _EntryModelID) _EntryModelID = value; OnPropertyChanged(); }
        }

    }
}
