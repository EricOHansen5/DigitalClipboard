using Microsoft.VisualStudio.TestTools.UnitTesting;
using DigitalClipboardAdmin.Controllers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using DigitalClipboardAdmin.Models;
using System.IO;

namespace DigitalClipboardAdmin.Controllers.Tests
{
    [TestClass()]
    public class DatastoreControllerTests
    {
        [TestMethod()]
        public void ReadDCLogsTest_Success()
        {
            var lst = DatastoreController.GetDCLogs();
            Assert.IsTrue(lst.Count >= 10);
        }

        [TestMethod()]
        public void ConvertDCLogsTest_Success()
        {
            var clst = DatastoreController.ConvertDCLogs();
            Assert.IsTrue(clst.Count >= 2);
        }

        [TestMethod()]
        public void GetDbQueryTest_Success()
        {
            IEnumerable<List<Object>> lst = DatastoreController.GetDbQuery(DatastoreController.QueryType.Device);
            var cLst = lst.ToList();
            Assert.IsTrue(cLst.Count >= 654);
        }

        [TestMethod()]
        public void ConvertToDeviceTest_Success()
        {
            //IEnumerable<List<Object>> lst = DatastoreController.GetDbQuery(DatastoreController.QueryType.Device);
            var dms = DatastoreController.ConvertToDevice();
            Assert.IsTrue(dms.Count >= 654);
        }

        [TestMethod()]
        public void SetDCLogsTest_Success()
        {
            DatastoreController.SetDCLogs();
            Assert.IsTrue(true);
        }

        [TestMethod()]
        public void SetJsonDBTest()
        {
            JsonStorageModel jsm = new JsonStorageModel();
            jsm.Entries = DatastoreController.ConvertDCLogs();
            jsm.Devices = DatastoreController.ConvertToDevice();
            jsm.Users = DatastoreController.ConvertToUser();
            (jsm.Mappings, jsm.NonMappings) = DatastoreController.CreateMapping(jsm.Entries, jsm.Devices, jsm.Users);
            Assert.IsTrue(DatastoreController.SetJsonDB(jsm));
        }

        [TestMethod()]
        public void ConvertToUserTest()
        {
            var ums = DatastoreController.ConvertToUser();
            Assert.IsTrue(ums.Count > 360);
        }

        [TestMethod()]
        public void ConvertToHRHTest()
        {
            var ums = DatastoreController.ConvertToHRH();
            Assert.IsTrue(ums.Count > 40);
        }

        [TestMethod()]
        public void ConvertToSoftwareTest()
        {
            var sw = DatastoreController.ConvertToSoftware();
            Assert.IsTrue(sw.Count > 200);
        }

        [TestMethod()]
        public void ConvertToSoftwareLicenseTest()
        {
            var sw = DatastoreController.ConvertToSoftwareLicense();
            Assert.IsTrue(sw.Count > 450);
        }

        [TestMethod()]
        public void ConvertToSoftwareMappedTest()
        {
            var sw = DatastoreController.ConvertToSoftwareMapped();
            Assert.IsTrue(sw.Count > 800);
        }
    }
}