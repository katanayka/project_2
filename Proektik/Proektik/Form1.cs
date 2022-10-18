using System.Data;
using System.Data.SQLite;
using System.IO;

namespace Proektik
{
    public partial class Form1 : Form
    {
        string cur_db_path = "C:\\Users\\artem\\source\\repos\\Proektik\\Proektik\\bipki.db";
        public Form1()
        {
            InitializeComponent();
            //Delete tabPage1 from tabControl1
            tabControl1.TabPages.Remove(tabPage1);
            open_db(cur_db_path);
        }

        private void button1_Click(object sender, EventArgs e)
        {
            open_db(open_file());
        }
        string open_file()
        {
            //Open window to select file .db
            OpenFileDialog ofd = new OpenFileDialog();
            ofd.Filter = "Database files (*.db)|*.db";
            ofd.ShowDialog();
            string path = ofd.FileName;
            return path;
        }
        void open_db(string path)
        {
            //Open connection to database
            SQLiteConnection conn = new SQLiteConnection("Data Source=" + path);
            conn.Open();
            //Clear tabControl1
            tabControl1.TabPages.Clear();
            //Create new tab for each table in database
            DataTable dt = conn.GetSchema("Tables");
            foreach (DataRow row in dt.Rows)
            {
                string tableName = row["TABLE_NAME"].ToString();
                SQLiteCommand cmd = new SQLiteCommand("SELECT * FROM " + tableName, conn);
                SQLiteDataAdapter da = new SQLiteDataAdapter(cmd);
                DataTable table = new DataTable();
                da.Fill(table);
                DataGridView dgv = new DataGridView();
                dgv.DataSource = table;
                TabPage tp = new TabPage(tableName);
                //Set size of dgv to size of tab
                dgv.Dock = DockStyle.Fill;
                tp.Controls.Add(dgv);
                tabControl1.TabPages.Add(tp);
            }
            conn.Close();
        }
    }
}