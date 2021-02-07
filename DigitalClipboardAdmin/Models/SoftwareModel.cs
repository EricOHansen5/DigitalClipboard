using DigitalClipboardAdmin.Controllers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DigitalClipboardAdmin.Models
{
    public class SoftwareModel:BaseClass
    {

        private string _ID;
        public string ID
        {
            get { return _ID; }
            set { if (value != _ID) _ID = value; OnPropertyChanged(); }
        }
        private string _Name;
        public string Name
        {
            get { return _Name; }
            set { if (value != _Name) _Name = value; OnPropertyChanged(); }
        }

        private List<string> _Notes;
        public List<string> Notes
        {
            get { return _Notes; }
            set { if (value != _Notes) _Notes = value; OnPropertyChanged(); }
        }

        private string _Location;
        public string Location
        {
            get { return _Location; }
            set { if (value != _Location) _Location = value; OnPropertyChanged(); }
        }
        private string _Source;
        public string Source
        {
            get { return _Source; }
            set { if (value != _Source) _Source = value; OnPropertyChanged(); }
        }
    }
}
