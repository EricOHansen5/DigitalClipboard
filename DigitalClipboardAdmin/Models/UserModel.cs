using DigitalClipboardAdmin.Controllers;

namespace DigitalClipboardAdmin.Models
{
    public class UserModel:BaseClass
    {

        private string _UserID;
        public string UserID
        {
            get { return _UserID; }
            set { if (value != _UserID) _UserID = value; OnPropertyChanged(); }
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
        public string FullName
        {
            get
            {
                return FirstName + " " + LastName;
            }
        }
    }
}
