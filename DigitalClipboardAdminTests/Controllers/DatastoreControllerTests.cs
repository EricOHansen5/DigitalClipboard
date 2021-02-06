using Microsoft.VisualStudio.TestTools.UnitTesting;
using DigitalClipboardAdmin.Controllers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using DigitalClipboardAdmin.Models;

namespace DigitalClipboardAdmin.Controllers.Tests
{
    [TestClass()]
    public class DatastoreControllerTests
    {
        [TestMethod()]
        public void ReadDCLogsTest_Success()
        {
            var lst = DatastoreController.ReadDCLogs();
            Assert.IsTrue(lst.Count == 3, "List was not equal to 3");
        }

        [TestMethod()]
        public void ConvertDCLogsTest_Success()
        {
            var lst = DatastoreController.ReadDCLogs();
            var clst = DatastoreController.ConvertDCLogs(lst);
            Assert.IsTrue(clst.Count == 2, "List was not equal to 3");
        }

        [TestMethod()]
        public void GetDbQueryTest_Success()
        {
            IEnumerable<List<Object>> lst = DatastoreController.GetDbQuery(DatastoreController.QueryType.Device);
            var cLst = lst.ToList();
            Assert.IsTrue(cLst.Count == 744);
        }

        [TestMethod()]
        public void ConvertToDeviceTest()
        {
            IEnumerable<List<Object>> lst = DatastoreController.GetDbQuery(DatastoreController.QueryType.Device);
            List<DeviceModel> dms = DatastoreController.ConvertToDevice(lst.ToList());
            Assert.IsTrue(dms.Count == 744);
        }
    }
}