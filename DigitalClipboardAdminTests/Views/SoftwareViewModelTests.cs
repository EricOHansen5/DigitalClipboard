using Microsoft.VisualStudio.TestTools.UnitTesting;
using DigitalClipboardAdmin.Views;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using DigitalClipboardAdmin.Controllers;

namespace DigitalClipboardAdmin.Views.Tests
{
    [TestClass()]
    public class SoftwareViewModelTests
    {
        [TestMethod()]
        public void GetSoftwareTest()
        {
            var sw = DatastoreController.ConvertToSoftware();
            var lic = DatastoreController.ConvertToSoftwareLicense();
            var map = DatastoreController.ConvertToSoftwareMapped();

            SoftwareViewModel svm = new SoftwareViewModel();
            svm.ID ="RIEMNB6228X";
            svm.GetSoftware(sw, lic, map);

            Assert.IsTrue(svm.Software.Count > 6);
        }
    }
}