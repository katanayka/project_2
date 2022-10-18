using System.Data;
using System.Data.SQLite;
using System.IO;
using System.Text.Json;
using Newtonsoft.Json;

namespace Proektik
{
    public partial class Form1 : Form
    {
        string cur_db_path = "C:\\Users\\artem\\source\\repos\\Proektik\\Proektik\\bipki.db";
        public Form1()
        {
            InitializeComponent();
            open_db(cur_db_path);
        }

        private void button1_Click(object sender, EventArgs e)
        {
            string Path = open_file();
            if (Path != null)
            {
                open_db(Path);
            }
        }
        string open_file()
        {
            //Open window to select file .db
            OpenFileDialog ofd = new OpenFileDialog();
            //If closed break
            ofd.Filter = "Database files (*.db)|*.db";
            if (ofd.ShowDialog() == DialogResult.Cancel)
                return null;
            string path = ofd.FileName;
            return path;
        }

        void open_db(string path)
        {
            //Open connection to database
            //If file not exist return null
            if (!File.Exists(path))
            {
                MessageBox.Show("File not exist");
                return;
            }
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

        private void button2_Click(object sender, EventArgs e)
        {
            if (button2.Text == ">>")
            {
                //Add 300px to right to form
                this.Width += 400;
                button2.Text = "<<";
                label1.Visible = true;
            }
            else
            {
                //Remove 300px from right to form
                this.Width -= 400;
                button2.Text = ">>";
                label1.Visible = false;
            }
        }
    }
}