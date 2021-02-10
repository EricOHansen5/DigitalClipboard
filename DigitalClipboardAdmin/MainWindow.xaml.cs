using DigitalClipboardAdmin.Controllers;
using DigitalClipboardAdmin.Models;
using DigitalClipboardAdmin.Views;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;
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


        private Dictionary<string, List<EntryModel>> _Entries;
        public Dictionary<string, List<EntryModel>> Entries
        {
            get { return _Entries; }
            set { if (value != _Entries) _Entries = value; OnPropertyChanged(); }
        }

        private List<EntryViewModel> _ViewEntries;
        public List<EntryViewModel> ViewEntries
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


        public MainWindow()
        {
            // Check / Create Dependencies
            (bool dcExist, bool jsonExist, bool dbExist) = DatastoreController.CheckDependecies();

            if (jsonExist)
            {
                // restore Mappings, nonMappings, Entries, Devices
                JsonStorageModel jsm = DatastoreController.GetJsonDB();
                Entries = jsm.Entries;
                Devices = jsm.Devices;
                Mappings = jsm.Mappings;
                NonMapped = jsm.NonMappings;
                Users = jsm.Users;
                HRHs = jsm.HRHs;

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

                // Merge Data
                (Mappings, NonMapped) = DatastoreController.CreateMapping(Entries, Devices);

                // Save Json Data
                JsonStorageModel jsm = new JsonStorageModel()
                {
                    Entries = this.Entries,
                    Devices = this.Devices,
                    Mappings = this.Mappings,
                    NonMappings = this.NonMapped,
                    Users = this.Users,
                    HRHs = this.HRHs
                };
                DatastoreController.SetJsonDB(jsm);
            }

            // Init view model
            ViewEntries = EntryViewModel.InitList(Entries, Devices, Users, HRHs);

            // Start Background Worker

            InitializeComponent();
            DataContext = this;

        }

        private void Device_Name_Click(object sender, RoutedEventArgs e)
        {
            tabControl.SelectedIndex = 1;
        }

        private void User_Name_Click(object sender, RoutedEventArgs e)
        {
            tabControl.SelectedIndex = 2;
        }

        private void HRH_Click(object sender, RoutedEventArgs e)
        {
            tabControl.SelectedIndex = 2;
        }

        private void Software_Click(object sender, RoutedEventArgs e)
        {
            tabControl.SelectedIndex = 3;
        }
    }
}
