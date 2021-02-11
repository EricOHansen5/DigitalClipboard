﻿using DigitalClipboardAdmin.Controllers;
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

        #region Properties
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
        #endregion

        public MainWindow()
        {
            // Check / Create Dependencies
            (bool dcExist, bool jsonExist, bool dbExist) = DatastoreController.CheckDependecies();

            if (jsonExist)
            {
                // restore Mappings, nonMappings, Entries, Devices
                this.jsm = DatastoreController.GetJsonDB();
                Entries = jsm.Entries;
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
                (Mappings, NonMapped) = DatastoreController.CreateMapping(Entries, Devices);

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

            // Init view model
            ViewEntries = EntryViewModel.InitList(Entries, Devices, Users, HRHs, Software, Licenses, SoftwareMappings);

            // Start Background Worker

            InitializeComponent();
            DataContext = this;

        }

        private void Device_Name_Click(object sender, RoutedEventArgs e)
        {
            tabControl.SelectedIndex = 1;
        }

        private void Software_Click(object sender, RoutedEventArgs e)
        {
            tabControl.SelectedIndex = 2;
        }

        private void Update_Notes_Click(object sender, RoutedEventArgs e)
        {
            Log.Add("Update_Notes_Click");
            EntryViewModel evm = dgEntries.SelectedItem as EntryViewModel;
            string note = evm.Device.Notes;
            Devices[evm.Device.Name].Notes = note;
            DatastoreController.SetJsonDB(this.jsm);
        }
    }
}
