using DigitalClipboardAdmin.Controllers;

namespace DigitalClipboardAdmin.Models
{
    public class HRHModel:BaseClass
    {

        private string _HolderID;
        public string HolderID
        {
            get { return _HolderID; }
            set { if (value != _HolderID) _HolderID = value; OnPropertyChanged(); }
        }
        private string _FirstName;
        public string FirstName
        {
            get { return _FirstName; }
            set { if (value != _FirstName) _FirstName = value; OnPropertyChanged(); }
        }
        private string _LastName;
        public string LastName
        {
            get { return _LastName; }
            set { if (value != _LastName) _LastName = value; OnPropertyChanged(); }
        }
    }
}
