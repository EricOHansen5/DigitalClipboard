using DigitalClipboardAdmin.Controllers;
using DigitalClipboardAdmin.Models;
using DigitalClipboardAdmin.Views;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;
using System.Timers;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace DigitalClipboardAdmin
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window, INotifyPropertyChanged
    {
        #region Notify Property Changed Members
        public event PropertyChangedEventHandler PropertyChanged;
        public void OnPropertyChanged([CallerMemberName] string name = "")
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        }
        #endregion

        #region Properties
        private Dictionary<string, List<EntryModel>> _Entries;
        public Dictionary<string, List<EntryModel>> Entries
        {
            get { return _Entries; }
            set { if (value != _Entries) _Entries = value; OnPropertyChanged(); }
        }

        private Dictionary<string, List<EntryModel>> _NewEntries;
        public Dictionary<string, List<EntryModel>> NewEntries
        {
            get { return _NewEntries; }
            set { if (value != _NewEntries) _NewEntries = value; OnPropertyChanged(); }
        }

        private ICollectionView _ViewEntries;
        public ICollectionView ViewEntries
        {
            get { return _ViewEntries; }
            set { if (value != _ViewEntries) _ViewEntries = value; OnPropertyChanged(); }
        }
        
        private Dictionary<string, DeviceModel> _Devices;
        public Dictionary<string, DeviceModel> Devices
        {
            get { return _Devices; }
            set { if (value != _Devices) _Devices = value; OnPropertyChanged(); }
        }

        private Dictionary<string, DeviceModel> _NewDevices;
        public Dictionary<string, DeviceModel> NewDevices
        {
            get { return _NewDevices; }
            set { if (value != _NewDevices) _NewDevices = value; OnPropertyChanged(); }
        }

        private Dictionary<string, UserModel> _Users;
        public Dictionary<string, UserModel> Users
        {
            get { return _Users; }
            set { if (value != _Users) _Users = value; OnPropertyChanged(); }
        }

        private Dictionary<string, HRHModel> _HRHs;
        public Dictionary<string, HRHModel> HRHs
        {
            get { return _HRHs; }
            set { if (value != _HRHs) _HRHs = value; OnPropertyChanged(); }
        }

        private Dictionary<string, MappedModel> _Mappings;
        public Dictionary<string, MappedModel> Mappings
        {
            get { return _Mappings; }
            set { if (value != _Mappings) _Mappings = value; OnPropertyChanged(); }
        }

        private Dictionary<string, List<EntryModel>> _NonMapped;
        public Dictionary<string, List<EntryModel>> NonMapped
        {
            get { return _NonMapped; }
            set { if (value != _NonMapped) _NonMapped = value; OnPropertyChanged(); }
        }

        private Dictionary<string, SoftwareModel> _Software;
        public Dictionary<string, SoftwareModel> Software
        {
            get { return _Software; }
            set { if (value != _Software) _Software = value; OnPropertyChanged(); }
        }
        
        private Dictionary<string, SoftwareLicenseModel> _Licenses;
        public Dictionary<string, SoftwareLicenseModel> Licenses
        {
            get { return _Licenses; }
            set { if (value != _Licenses) _Licenses = value; OnPropertyChanged(); }
        }
        
        private Dictionary<string, SoftwareMappedModel> _SoftwareMappings;
        public Dictionary<string, SoftwareMappedModel> SoftwareMappings
        {
            get { return _SoftwareMappings; }
            set { if (value != _SoftwareMappings) _SoftwareMappings = value; OnPropertyChanged(); }
        }

        public JsonStorageModel jsm { get; set; }

        private Timer timer;
        private FileInfo jsonFileinfo;
        private FileInfo accessFileinfo;
        private FileInfo[] dcFileinfo;

        #endregion

        public MainWindow(bool isUpdateDB = false)
        {
            // Check / Create Dependencies
            (dcFileinfo, jsonFileinfo, accessFileinfo) = DatastoreController.CheckDependecies();

            if (jsonFileinfo != null && jsonFileinfo.Length > 0)
            {
                // restore Mappings, nonMappings, Entries, Devices
                this.jsm = DatastoreController.GetJsonDB();
                // Populate
                Entries = jsm.Entries;
                NewEntries = DatastoreController.ConvertDCLogs();
                Merge_DC_Entries(NewEntries);



                Devices = jsm.Devices;
                Mappings = jsm.Mappings;
                NonMapped = jsm.NonMappings;
                Users = jsm.Users;
                HRHs = jsm.HRHs;
                Software = jsm.Software;
                Licenses = jsm.Licenses;
                SoftwareMappings = jsm.SoftwareMappings;
                Log.Add("Jsm Restore Complete");
            }
            else
            {
                // Get Data from Logs (insert null to read DC logs & convert)
                Entries = DatastoreController.ConvertDCLogs();
                
                // Get Data from Access DB
                Devices = DatastoreController.ConvertToDevice();
                Users = DatastoreController.ConvertToUser();
                HRHs = DatastoreController.ConvertToHRH();
                Software = DatastoreController.ConvertToSoftware();
                Licenses = DatastoreController.ConvertToSoftwareLicense();
                SoftwareMappings = DatastoreController.ConvertToSoftwareMapped();

                // Merge Data
                (Mappings, NonMapped) = DatastoreController.CreateMapping(Entries, Devices, Users);

                // Save Json Data
                this.jsm = new JsonStorageModel()
                {
                    Entries = this.Entries,
                    Devices = this.Devices,
                    Mappings = this.Mappings,
                    NonMappings = this.NonMapped,
                    Users = this.Users,
                    HRHs = this.HRHs,
                    Software = this.Software,
                    Licenses = this.Licenses,
                    SoftwareMappings = this.SoftwareMappings
                };
                DatastoreController.SetJsonDB(jsm);
            }
            Predicate<object> EntryFilter = new Predicate<object>(this.EntryFilter);

            // Init view model
            ViewEntries = EntryViewModel.InitList(Entries, Devices, Users, HRHs, Software, Licenses, SoftwareMappings, EntryFilter);
            ViewEntries.SortDescriptions.Add(new SortDescription("dateTime", ListSortDirection.Descending));
            //ViewEntries = (ICollectionView)ViewEntries.OrderByDescending(x => x.dateTime).ToList();
            ViewEntries.Filter = new Predicate<object>(this.Filter);

            // Start Background Worker
            //timer = new Timer(5000);
            //timer.Elapsed += new ElapsedEventHandler(async(s,e) => await OnTimedEvent());
            //timer.Enabled = true;

            InitializeComponent();
            DataContext = this;

        }

        private void Merge_DC_Entries(Dictionary<string, List<EntryModel>> newEntries)
        {
            // Check if dictionarys exist
            if(this.Entries != null && newEntries != null)
            {                
                // Iterates through all processed entries
                foreach (KeyValuePair<string, List<EntryModel>> entry in newEntries)
                {
                    // Check if new entries have more entries than processed ones
                    if (this.Entries.ContainsKey(entry.Key))// && this.Entries[entry.Key].Count != entry.Value.Count)
                    {

                        Merge_Lists(this.Entries[entry.Key], entry.Value);
                    }
                }

            }
        }

        private void Merge_Lists(List<EntryModel> procList, List<EntryModel> newList)
        {
            foreach (EntryModel nItem in newList)
            {
                EntryModel em = procList.FirstOrDefault(x => x.dateTime == nItem.dateTime);
                if (em != null)
                {
                    //procList.Add(new EntryModel(nItem));
                    int ix = procList.IndexOf(em);
                    procList[ix] = new EntryModel(nItem);

                }
            }
        }

        private async Task OnTimedEvent()
        {
            if (dcFileinfo == null || jsonFileinfo == null || accessFileinfo == null)
            {
                dcFileinfo = ((FileInfo[])DatastoreController.GetFileInfo(DatastoreController.filepath.DCLogs))
                    .OrderBy(x => x.LastWriteTime).ToArray();
                jsonFileinfo = (FileInfo)DatastoreController.GetFileInfo(DatastoreController.filepath.JSONFile);
                accessFileinfo = (FileInfo)DatastoreController.GetFileInfo(DatastoreController.filepath.DBFile);
            }
            else
            {
                FileInfo[] curDCFileinfo = (FileInfo[])DatastoreController.GetFileInfo(DatastoreController.filepath.DCLogs);
                FileInfo curAccessFileinfo = (FileInfo)DatastoreController.GetFileInfo(DatastoreController.filepath.DBFile);
                curDCFileinfo = curDCFileinfo.OrderBy(x => x.LastWriteTime).ToArray();
                if(curDCFileinfo.Last().LastWriteTime > dcFileinfo.Last().LastWriteTime)
                {
                    NewEntries = DatastoreController.ConvertDCLogs();

                }

                if(curAccessFileinfo.LastWriteTime > accessFileinfo.LastWriteTime)
                {
                    NewDevices = DatastoreController.ConvertToDevice();
                }
            }
        }

        private void Device_Name_Click(object sender, RoutedEventArgs e)
        {
            tabControl.SelectedIndex = 1;
        }
        private void Software_Click(object sender, RoutedEventArgs e)
        {
            tabControl.SelectedIndex = 2;
        }
        private void All_Entries_Click(object sender, RoutedEventArgs e)
        {
            tabControl.SelectedIndex = 3;
        }

        private void Update_Notes_Click(object sender, RoutedEventArgs e)
        {
            Log.Add("Update_Notes_Click");
            EntryViewModel evm = dgEntries.SelectedItem as EntryViewModel;
            string note = evm.Device.Notes;
            Devices[evm.Device.Name].Notes = note;
            DatastoreController.SetJsonDB(this.jsm);
        }


        #region Search
        private void Search_Enter_Click(object sender, KeyEventArgs e)
        {
            
            if(e.Key == Key.Enter)
            {
                if ((sender as TextBox).Name == "txtSearch")
                {
                    FilterString = (sender as TextBox).Text;
                }
                else if ((sender as TextBox).Name == "txtSearch_All")
                {
                    FilterStringAllEntries = (sender as TextBox).Text;
                }
            }
        }

        private string _FilterString;
        public string FilterString
        {
            get { return _FilterString; }
            set { 
                if (value != _FilterString) 
                    _FilterString = value; 
                OnPropertyChanged(); 
                FilterCollection(); 
            }
        }
        private string _FilterStringAllEntries;
        public string FilterStringAllEntries
        {
            get { return _FilterStringAllEntries; }
            set { 
                if (value != _FilterStringAllEntries) 
                    _FilterStringAllEntries = value; 
                OnPropertyChanged();
                FilterCollection();
            }
        }

        private void FilterCollection()
        {
            if(_ViewEntries != null)
            {
                _ViewEntries.Refresh();
            }
            if(dgEntries != null && dgEntries.SelectedItem != null)
            {
                (dgEntries.SelectedItem as EntryViewModel).EntryList.Refresh();
            }
        }

        public bool Filter(object obj)
        {
            var data = obj as EntryViewModel;
            if(data != null)
            {
                if (!string.IsNullOrEmpty(_FilterString))
                {
                    string cleanString = _FilterString.ToLower();

                    return data.First.ToLower().Contains(cleanString) || data.Last.ToLower().Contains(cleanString) || data.ECN.ToLower().Contains(cleanString) || data.FullName.ToLower().Contains(cleanString);
                }
                return true;
            }
            return false;
        }
        public bool EntryFilter(object obj)
        {
            EntryModel data = obj as EntryModel;
            if (data != null)
            {
                if (!string.IsNullOrEmpty(_FilterStringAllEntries))
                {
                    string cleanString = _FilterStringAllEntries.ToLower();

                    return data.firstName.ToLower().Contains(cleanString) || data.lastName.ToLower().Contains(cleanString) || data.ECN.ToLower().Contains(cleanString) || data.fullName.ToLower().Contains(cleanString);
                }
                return true;
            }
            return false;
        }
        #endregion

    }
}
