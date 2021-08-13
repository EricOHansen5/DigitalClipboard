using Microsoft.VisualStudio.TestTools.UnitTesting;
using DigitalClipboardAdmin.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DigitalClipboardAdmin.Models.Tests
{
    [TestClass()]
    public class DeviceModelTests
    {
        [TestMethod()]
        public void ParseECNTest_Success()
        {
            string name = "MRESNNB4953X";
            var result = DeviceModel.ParseECN(name);
            Assert.IsTrue(result == "4953");
        }

        [TestMethod()]
        public void ParseECNTest_Failure()
        {
            string name = "MRESNNB";
            var result = DeviceModel.ParseECN(name);
            Assert.IsTrue(result == "");
        }

        [TestMethod()]
        public void ContainsECNTest_Success()
        {
            Assert.IsTrue(DeviceModel.ContainsECN("5201", "MRESNNB5201X"));
        }
    }
}