using DigitalClipboardAdmin.Views;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DigitalClipboardAdmin.Models
{
    public class JsonStorageModel
    {
        public Dictionary<string, List<EntryModel>> Entries;
        public Dictionary<string, DeviceModel> Devices;
        public Dictionary<string, MappedModel> Mappings;
        public Dictionary<string, List<EntryModel>> NonMappings;
        public Dictionary<string, UserModel> Users;
        public Dictionary<string, HRHModel> HRHs;
        public Dictionary<string, SoftwareModel> Software;
        public Dictionary<string, SoftwareLicenseModel> Licenses;
        public Dictionary<string, SoftwareMappedModel> SoftwareMappings;
    }
}
