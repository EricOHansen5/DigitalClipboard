using DigitalClipboardAdmin.Controllers;
using DigitalClipboardAdmin.Models;
using DigitalClipboardAdmin.Shared;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Data;

namespace DigitalClipboardAdmin.Views
{
    public class EntryViewModel:BaseClass
    {
        public EntryViewModel(KeyValuePair<string, List<EntryModel>> em)
        {
            this.Key = em.Key;
            this.Entries = em.Value.OrderByDescending(x => x.dateTime).ToList();
            EntryModel infoM = EntryModel.GetInfo(em.Value);
            this.ECN = infoM.ECN;
            this.First = infoM.firstName;
            this.Last = infoM.lastName;
            this.Tech = infoM.techName;
            this.Status = infoM.checkIn ? Constants.CheckedIn : Constants.CheckedOut;
            EntryModel mostRecent = EntryModel.GetMostRecent(em.Value);
            this.dateTime = mostRecent.dateTime;
            this.Reason = string.IsNullOrWhiteSpace(mostRecent.reason) ? "" : mostRecent.reason;
        }

        public static ICollectionView InitList(
            Dictionary<string, List<EntryModel>> entries, 
            Dictionary<string, DeviceModel> devices, 
            Dictionary<string, UserModel> users, 
            Dictionary<string, HRHModel> hrhs, 
            Dictionary<string, SoftwareModel> software, 
            Dictionary<string, SoftwareLicenseModel> licenses, 
            Dictionary<string, SoftwareMappedModel> softwareMappings,
            Predicate<object> EntryFilter)
        {
            Log.Add("InitList EntryViewModel");
            var l = new List<EntryViewModel>();
            
            foreach (var item in entries)
            {
                EntryViewModel e = new EntryViewModel(item);
                e.EntryList.Filter = EntryFilter;
                e.SetMappings(devices, users, hrhs, software, licenses, softwareMappings);
                l.Add(e);
            }
            return CollectionViewSource.GetDefaultView(l);
        }

        public void SetMappings
            (Dictionary<string, DeviceModel> devices, Dictionary<string, UserModel> users, Dictionary<string, 
                HRHModel> hrhs, Dictionary<string, SoftwareModel> software, Dictionary<string, SoftwareLicenseModel> licenses, 
            Dictionary<string, SoftwareMappedModel> softwareMappings)
        {
            foreach (var item in devices.Values)
            {
                if (item.ECN == this.Key)
                {
                    this.Device = item;
                    if (users.ContainsKey(this.Device.UserID))
                    {
                        this.User = users[this.Device.UserID];
                        this.First = users[this.Device.UserID].FirstName;
                        this.Last = users[this.Device.UserID].LastName;
                    }
                    if (hrhs.ContainsKey(this.Device.HRH_ID))
                    {
                        this.HRH = hrhs[this.Device.HRH_ID];
                    }
                }

                SoftwareViewModel svm = new SoftwareViewModel() { ID = item.Name };
                svm.GetSoftware(software, licenses, softwareMappings);
                item.SoftwareViewModel = svm;            
            }

        }

        private string _Key;
        public string Key
        {
            get { return _Key; }
            set { if (value != _Key) _Key = value; OnPropertyChanged(); }
        }

        private List<EntryModel> _Entries;
        public List<EntryModel> Entries
        {
            get { return _Entries; }
            set { if (value != _Entries) _Entries = value; OnPropertyChanged(); }
        }
        public ICollectionView EntryList
        {
            get { return CollectionViewSource.GetDefaultView(Entries); }
        }

        private string _Status;
        public string Status
        {
            get { return _Status; }
            set { if (value != _Status) _Status = value; OnPropertyChanged(); }
        }

        private string _ECN;
        public string ECN
        {
            get { return _ECN; }
            set { if (value != _ECN) _ECN = value; OnPropertyChanged(); }
        }

        private string _First;
        public string First
        {
            get { return _First; }
            set { if (value != _First) _First = value; OnPropertyChanged(); }
        }
        
        private string _Last;
        public string Last
        {
            get { return _Last; }
            set { if (value != _Last) _Last = value; OnPropertyChanged(); }
        }
        
        public string FullName
        {
            get { return string.Format("{0} {1}", First, Last); }
        }
       
        private string _Tech;
        public string Tech
        {
            get { return _Tech; }
            set { if (value != _Tech) _Tech = value; OnPropertyChanged(); }
        }
        
        private DateTime _dateTime;
        public DateTime dateTime
        {
            get { return _dateTime; }
            set { if (value != _dateTime) _dateTime = value; OnPropertyChanged(); }
        }

        private string _Reason;
        public string Reason
        {
            get { return _Reason; }
            set { if (value != _Reason) _Reason = value; OnPropertyChanged(); }
        }

        private DeviceModel _Device;
        public DeviceModel Device
        {
            get { return _Device; }
            set { if (value != _Device) _Device = value; OnPropertyChanged(); }
        }
        private UserModel _User;
        public UserModel User
        {
            get { return _User; }
            set { if (value != _User) _User = value; OnPropertyChanged(); }
        }
        private HRHModel _HRH;
        public HRHModel HRH
        {
            get { return _HRH; }
            set { if (value != _HRH) _HRH = value; OnPropertyChanged(); }
        }
    }
}
