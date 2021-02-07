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
        private DeviceModel _DeviceModel;
        public DeviceModel DeviceModel
        {
            get { return _DeviceModel; }
            set { if (value != _DeviceModel) _DeviceModel = value; OnPropertyChanged(); }
        }

        // ECN
        private string _EntryModelID;
        public string EntryModelID
        {
            get { return _EntryModelID; }
            set { if (value != _EntryModelID) _EntryModelID = value; OnPropertyChanged(); }
        }
        private EntryModel _EntryModel;
        public EntryModel EntryModel
        {
            get { return _EntryModel; }
            set { if (value != _EntryModel) _EntryModel = value; OnPropertyChanged(); }
        }

    }
}
