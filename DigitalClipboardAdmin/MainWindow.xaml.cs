using DigitalClipboardAdmin.Controllers;
using DigitalClipboardAdmin.Models;
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

        private List<EntryModel> _Entries;
        public List<EntryModel> Entries
        {
            get { return _Entries; }
            set { if (value != _Entries) _Entries = value; OnPropertyChanged(); }
        }

        private List<DeviceModel> _Devices = new List<DeviceModel>();
        public List<DeviceModel> Devices
        {
            get { return _Devices; }
            set { if (value != _Devices) _Devices = value; OnPropertyChanged(); }
        }

        private List<MappedModel> _Mappings;
        public List<MappedModel> Mappings
        {
            get { return _Mappings; }
            set { if (value != _Mappings) _Mappings = value; OnPropertyChanged(); }
        }

        private List<EntryModel> _NonMapped = new List<EntryModel>();
        public List<EntryModel> NonMapped
        {
            get { return _NonMapped; }
            set { if (value != _NonMapped) _NonMapped = value; OnPropertyChanged(); }
        }

        public MainWindow()
        {
            // Check / Create Dependencies
            DatastoreController.CheckDependecies();

            // Get Data from Logs (insert null to read DC logs & convert)
            Entries = DatastoreController.ConvertDCLogs();
            
            // Get Data from Access DB
            Devices = DatastoreController.ConvertToDevice();
            
            // Merge Data
            (Mappings, NonMapped) = DatastoreController.CreateMapping(Entries, Devices);

            // Start Background Worker
            
            InitializeComponent();
            DataContext = this;




        }
    }
}
