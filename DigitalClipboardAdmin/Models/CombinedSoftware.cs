using DigitalClipboardAdmin.Controllers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DigitalClipboardAdmin.Models
{
    public class CombinedSoftware:BaseClass
    {
        public CombinedSoftware(SoftwareModel software, SoftwareLicenseModel license)
        {
            this.Software = software;
            this.License = license;
        }


        private SoftwareModel _Software;
        public SoftwareModel Software
        {
            get { return _Software; }
            set { if (value != _Software) _Software = value; OnPropertyChanged(); }
        }
        private SoftwareLicenseModel _License;
        public SoftwareLicenseModel License
        {
            get { return _License; }
            set { if (value != _License) _License = value; OnPropertyChanged(); }
        }
    
        public string Name
        {
            get
            {
                return string.Format("{0} {1}", Software.Name, License.Version);
            }
        }
    }
}
