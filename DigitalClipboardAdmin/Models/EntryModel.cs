using DigitalClipboardAdmin.Controllers;
using DigitalClipboardAdmin.Shared;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DigitalClipboardAdmin.Models
{
    public class EntryModel : BaseClass
    {
        public EntryModel()
        {

        }

        public EntryModel(EntryModel entry)
        {
            this.dateTime = entry.dateTime;
            this.checkIn = entry.checkIn;
            this.barcode = entry.barcode;
            this.ECN = entry.ECN;
            this.firstName = entry.firstName;
            this.lastName = entry.lastName;
            this.techName = entry.techName;
            this.reason = entry.reason;
            this.note = entry.note;
        }

        public static int PropertyCount = 6;

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

        public string status
        {
            get
            {
                return checkIn ? Constants.CheckIn : Constants.CheckOut;
            }
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

        public string fullName
        {
            get { return string.Format("{0} {1}", firstName, lastName); }
        }

        private string _techName;
        public string techName
        {
            get { return _techName; }
            set { if (value != _techName) _techName = value; OnPropertyChanged(); }
        }

        private string _reason;
        public string reason
        {
            get { return _reason; }
            set { if (value != _reason) _reason = value; OnPropertyChanged(); }
        }

        private string _note;
        public string note
        {
            get { return _note; }
            set { if (value != _note) _note = value; OnPropertyChanged(); }
        }

        private string _signaturePath;
        public string signaturePath
        {
            get { return _signaturePath; }
            set { if (value != _signaturePath) _signaturePath = value; OnPropertyChanged(); }
        }

        public string DisplayString
        {
            get { return string.Format("{0} - {1}", dateTime.ToString("g"), ECN); }
        }

        public static string GetBarcode(List<EntryModel> list)
        {
            if (list.Count > 0)
                return list[0].barcode;
            return null;
        }

        public static EntryModel GetMostRecent(List<EntryModel> list)
        {
            EntryModel tempEM = null;
            if (list.Count == 0 || list == null)
                return null;

            foreach (var item in list)
            {
                if (tempEM == null)
                    tempEM = item;

                if (tempEM.dateTime < item.dateTime)
                {
                    tempEM = item;
                }
            }
            return tempEM;
        }

        public static EntryModel GetInfo(List<EntryModel> list)
        {
            if (list != null && list.Count > 0)
                return list[0];
            return null;
        }
    }
}
