using DigitalClipboardAdmin.Controllers;
using DigitalClipboardAdmin.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DigitalClipboardAdmin.Views
{
    public class EntryViewModel:BaseClass
    {

        public EntryViewModel(KeyValuePair<string, List<EntryModel>> em)
        {
            this.Key = em.Key;
            this.Entries = em.Value;
            EntryModel infoM = EntryModel.GetInfo(em.Value);
            this.ECN = infoM.ECN;
            this.First = infoM.firstName;
            this.Last = infoM.lastName;
            this.dateTime = EntryModel.GetMostRecent(em.Value).dateTime;
            this.Tech = infoM.techName;
            this.Status = infoM.checkIn ? "Checked In" : "Checked Out";
        }

        public static List<EntryViewModel> InitList(Dictionary<string, List<EntryModel>> lst, Dictionary<string, DeviceModel> devices, Dictionary<string, UserModel> users, Dictionary<string, HRHModel> hrhs)
        {
            var l = new List<EntryViewModel>();
            foreach (var item in lst)
            {
                EntryViewModel e = new EntryViewModel(item);
                e.SetMappings(devices, users, hrhs);
                l.Add(e);
            }
            return l;
        }

        public void SetMappings(Dictionary<string, DeviceModel> devices, Dictionary<string, UserModel> users, Dictionary<string, HRHModel> hrhs)
        {
            foreach (var item in devices.Values)
            {
                if (item.ECN == this.Key)
                {
                    this.Device = item;
                    if (users.ContainsKey(this.Device.UserID))
                    {
                        this.User = users[this.Device.UserID];
                    }
                    if (hrhs.ContainsKey(this.Device.HRH_ID))
                    {
                        this.HRH = hrhs[this.Device.HRH_ID];
                    }
                }
            
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
