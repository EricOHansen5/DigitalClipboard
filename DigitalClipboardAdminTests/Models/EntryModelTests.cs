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
    public class EntryModelTests
    {
        [TestMethod()]
        public void GetBarcodeTest()
        {
            List<EntryModel> lst = new List<EntryModel>()
            {
                new EntryModel()
                {
                    barcode = "1234",
                    ECN = "5555"
                },
                new EntryModel()
                {
                    barcode = "1234",
                    ECN = "5555"
                },
                new EntryModel()
                {
                    barcode = "1234",
                    ECN = "5555"
                }
            };


            Assert.IsTrue(EntryModel.GetBarcode(lst) == "1234");
        }

        [TestMethod()]
        public void GetMostRecentTest()
        {
            List<EntryModel> lst = new List<EntryModel>()
            {
                new EntryModel()
                {
                    barcode = "1234",
                    ECN = "5555",
                    dateTime = DateTime.Today.AddDays(-1)
                },
                new EntryModel()
                {
                    barcode = "1234",
                    ECN = "5555",
                    dateTime = DateTime.Today.AddDays(-3)
                },
                new EntryModel()
                {
                    barcode = "1234",
                    ECN = "5555",
                    dateTime = DateTime.Today.AddDays(0)
                }
            };

            var t = EntryModel.GetMostRecent(lst);
            Assert.IsTrue(t.dateTime == DateTime.Today.AddDays(3));
        }
    }
}