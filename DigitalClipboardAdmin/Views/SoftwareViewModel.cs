using DigitalClipboardAdmin.Controllers;
using DigitalClipboardAdmin.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DigitalClipboardAdmin.Views
{
    public class SoftwareViewModel:BaseClass
    {

        private string _ID;
        public string ID
        {
            get { return _ID; }
            set { if (value != _ID) _ID = value; OnPropertyChanged(); }
        }
        #region Common Properties
        private List<SoftwareMappedModel> _Maps;
        public List<SoftwareMappedModel> Maps
        {
            get { return _Maps; }
            set { if (value != _Maps) _Maps = value; OnPropertyChanged(); }
        }
        private List<SoftwareLicenseModel> _Licenses;
        public List<SoftwareLicenseModel> Licenses
        {
            get { return _Licenses; }
            set { if (value != _Licenses) _Licenses = value; OnPropertyChanged(); }
        }
        private List<SoftwareModel> _Software;
        public List<SoftwareModel> Software
        {
            get { return _Software; }
            set { if (value != _Software) _Software = value; OnPropertyChanged(); }
        }

        private List<CombinedSoftware> _CombinedSoftware;
        public List<CombinedSoftware> CombinedSoftware
        {
            get { return _CombinedSoftware; }
            set { if (value != _CombinedSoftware) _CombinedSoftware = value; OnPropertyChanged(); }
        }
        #endregion

        private CombinedSoftware _Selected;
        public CombinedSoftware Selected
        {
            get { return _Selected; }
            set { if (value != _Selected) _Selected = value; OnPropertyChanged(); }
        }


        public void GetSoftware(Dictionary<string, SoftwareModel> software, Dictionary<string, SoftwareLicenseModel> licenses, Dictionary<string, SoftwareMappedModel> mappings)
        {
            Maps = new List<SoftwareMappedModel>();
            Licenses = new List<SoftwareLicenseModel>();
            Software = new List<SoftwareModel>();
            CombinedSoftware = new List<CombinedSoftware>();

            foreach (var map in mappings.Values)
            {
                // If map matches this ID
                // Get all licenses associated with this name
                // Get all software associated with those licenses
                if (map.DeviceName == this.ID)
                {
                    this.Maps.Add(map);
                    var lic = licenses[map.LicenseID];
                    this.Licenses.Add(lic);
                    this.Software.Add(software[lic.SoftwareID]);

                    CombinedSoftware.Add(new CombinedSoftware(software[lic.SoftwareID], lic));
                }
            }
        }
    }
}
