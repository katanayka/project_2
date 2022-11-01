using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Microsoft.Data.Sqlite;

namespace WinFormsApp3
{
    public partial class DB : Form
    {
        public DB()
        {
            InitializeComponent();
            //If no file bipki.db exists, select it by user and copy to current directory
            if (!System.IO.File.Exists("bipki.db"))
            {
                OpenFileDialog openFileDialog1 = new OpenFileDialog();
                openFileDialog1.Filter = "SQLite Database|*.db";
                openFileDialog1.Title = "Select a SQLite Database";
                if (openFileDialog1.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    System.IO.File.Copy(openFileDialog1.FileName, "bipki.db");
                }
            }
            //Create connection to DB
            SqliteConnection db = new SqliteConnection("Data Source=bipki.db");
            //Open connection
            db.Open();
            //Add to tabs all tables from DB
            SqliteCommand cmd = new SqliteCommand("SELECT name FROM sqlite_master WHERE type='table'", db);
            SqliteDataReader rdr = cmd.ExecuteReader();
            while (rdr.Read())
            {
                TabPage tab = new TabPage(rdr.GetString(0));
                tab.Name = rdr.GetString(0);
                tabControl1.TabPages.Add(tab);
            }
            //Get all data from db and add to tabs datagridview and set primary key to orange color
            foreach (TabPage tab in tabControl1.TabPages)
            {
                SqliteCommand cmd2 = new SqliteCommand("SELECT * FROM " + tab.Name, db);
                SqliteDataReader rdr2 = cmd2.ExecuteReader();
                DataTable dt = new DataTable();
                dt.Load(rdr2);
                DataGridView dgv = new DataGridView();
                dgv.DataSource = dt;
                dgv.Dock = DockStyle.Fill;
                tab.Controls.Add(dgv);
                SqliteCommand cmd3 = new SqliteCommand("PRAGMA table_info(" + tab.Name + ")", db);
                SqliteDataReader rdr3 = cmd3.ExecuteReader();
                while (rdr3.Read())
                {
                    if (rdr3.GetInt32(5) == 1)
                    {
                        //if there at least one row
                        if (dgv.Rows.Count > 0)
                        {
                            //set primary key to orange color
                            dgv.Rows[0].Cells[rdr3.GetInt32(0)].Style.BackColor = Color.Orange;
                        }
                    }
                }
            }
            //Close connection
            db.Close();
            //set each tab to center
            foreach (TabPage tab in tabControl1.TabPages)
            {
                tab.Left = (tabControl1.ClientSize.Width - tab.Width) / 2;
            }
            

        }
        private void DB_Load(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            //Clear faculties and students table
            SqliteConnection db = new SqliteConnection("Data Source=bipki.db");
            db.Open();
            SqliteCommand cmd = new SqliteCommand("DELETE FROM faculties", db);
            SqliteCommand cmd2 = new SqliteCommand("DELETE FROM students", db);
            cmd2.ExecuteNonQuery();
            cmd.ExecuteNonQuery();
            db.Close();

        }

        private void button3_Click(object sender, EventArgs e)
        {
            //Show hidden Form1
            Form1 form1 = new Form1();
            form1.Show();
            //Hide this form
            this.Hide();

        }

        private void button2_Click(object sender, EventArgs e)
        {
            //clear teamStudent
            SqliteConnection db = new SqliteConnection("Data Source=bipki.db");
            db.Open();
            SqliteCommand cmd = new SqliteCommand("DELETE FROM teamStudent", db);
            cmd.ExecuteNonQuery();
            db.Close();
            
        }
    }
}
