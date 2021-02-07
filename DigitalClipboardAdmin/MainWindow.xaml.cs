using DigitalClipboardAdmin.Controllers;
using DigitalClipboardAdmin.Models;
using System;
using System.Collections.Generic;
using System.Linq;
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
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            // Get Data from Logs (insert null to read DC logs & convert)
            List<EntryModel> Entries = DatastoreController.ConvertDCLogs();
            
            // Get Data from Access DB
            List<DeviceModel> Devices = DatastoreController.ConvertToDevice();
            
            // Merge Data
            List<MappedModel> Mappings = DatastoreController.CreateMapping(Entries, Devices);

            // Start Background Worker
             

            InitializeComponent();
            DataContext = this;

        }
    }
}
