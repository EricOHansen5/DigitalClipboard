using DigitalClipboardAdmin.Controllers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DigitalClipboardAdmin.Models
{
    public class EntryModel : BaseClass
    {

        public static int PropertyCount = 6;
        public static string CheckInStr = "--IN --";
        public static string CheckOutStr = "--OUT--";
        public static string EmptyTechStr = "no_tech";

        private DateTime _dateTime;
        public DateTime dateTime
        {
            get { return _dateTime; }
            set { if (value != _dateTime) _dateTime = value; OnPropertyChanged(); }
        }

        private bool _checkIn;
        public bool checkIn
        {
            get { return _checkIn; }
            set { if (value != _checkIn) _checkIn = value; OnPropertyChanged(); }
        }

        private string _barcode;
        public string barcode
        {
            get { return _barcode; }
            set { if (value != _barcode) _barcode = value; OnPropertyChanged(); }
        }

        private string _ECN;
        public string ECN
        {
            get { return _ECN; }
            set { if (value != _ECN) _ECN = value; OnPropertyChanged(); }
        }

        private string _firstName;
        public string firstName
        {
            get { return _firstName; }
            set { if (value != _firstName) _firstName = value; OnPropertyChanged(); }
        }

        private string _lastName;
        public string lastName
        {
            get { return _lastName; }
            set { if (value != _lastName) _lastName = value; OnPropertyChanged(); }
        }

        private string _techName;
        public string techName
        {
            get { return _techName; }
            set { if (value != _techName) _techName = value; OnPropertyChanged(); }
        }

    }
}
