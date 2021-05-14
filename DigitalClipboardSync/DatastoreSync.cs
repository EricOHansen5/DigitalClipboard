using DigitalClipboardAdmin.Models;
using DigitalClipboardAdmin.Controllers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DigitalClipboardSync
{
    public class DatastoreSync
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("Data Sync In Progress...");

            // Get Data from Logs (insert null to read DC logs & convert)
            var vEntries = DatastoreController.ConvertDCLogs();

            // Get Data from Access DB
            var vDevices = DatastoreController.ConvertToDevice();
            var vUsers = DatastoreController.ConvertToUser();
            var vHRHs = DatastoreController.ConvertToHRH();
            var vSoftware = DatastoreController.ConvertToSoftware();
            var vLicenses = DatastoreController.ConvertToSoftwareLicense();
            var vSoftwareMappings = DatastoreController.ConvertToSoftwareMapped();

            // Merge Data
            (var vMappings, var vNonMapped) = DatastoreController.CreateMapping(vEntries, vDevices, vUsers);

            // Save Json Data
            var jsm = new JsonStorageModel()
            {
                Entries = vEntries,
                Devices = vDevices,
                Mappings = vMappings,
                NonMappings = vNonMapped,
                Users = vUsers,
                HRHs = vHRHs,
                Software = vSoftware,
                Licenses = vLicenses,
                SoftwareMappings = vSoftwareMappings
            };
            DatastoreController.SetJsonDB(jsm);

            Console.WriteLine("Data Sync Complete.");
        }
    }
}
