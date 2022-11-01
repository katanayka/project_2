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
using static System.ComponentModel.Design.ObjectSelectorEditor;

namespace WinFormsApp3
{
    public partial class Student : Form
    {
        int Selected_row_index = 0;
        int Id = -1;
        public string Student_Name = "";
        public Student()
        {
            InitializeComponent();
            //Prettify button1
            button1.FlatStyle = FlatStyle.Flat;
            button1.FlatAppearance.BorderSize = 0;
            //Clear datagridview
            dataGridView1.Rows.Clear();

        }

        private void dataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Boolean Selecter = false;
            //Add name of selected docx file to datagridview
            OpenFileDialog openFileDialog1 = new OpenFileDialog();
            openFileDialog1.Filter = "Word Documents|*.docx";
            openFileDialog1.Title = "Select a Word Document";
            if (openFileDialog1.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                //Open Set_Team.cs to set team_id
                Set_Team set_Team = new Set_Team();
                set_Team.ShowDialog();
                //Get team_id from Set_Team.cs
                int team_id = set_Team.team_id;
                if (set_Team.DialogResult == DialogResult.OK)
                {
                    label4.Text = team_id.ToString();
                    //Get name of selected file without path
                    string name = openFileDialog1.SafeFileName;
                    //Add name to datagridview
                    dataGridView1.Rows.Add(name);
                    //Copy selected file to folder Feedback
                    //If file with same name already exists, dont copy
                    string path = System.IO.Path.Combine(Environment.CurrentDirectory, "Feedback");
                    string path2 = System.IO.Path.Combine(path, openFileDialog1.SafeFileName);
                    if (!System.IO.File.Exists(path2))
                    {
                        System.IO.File.Copy(openFileDialog1.FileName, path2);
                    }
                    //If team with team_id doesnt exist in teams table create it by adding name
                    using (var db = new SqliteConnection("Data Source=bipki.db"))
                    {
                        db.Open();
                        var selectCmd = db.CreateCommand();
                        selectCmd.CommandText = "SELECT * FROM teams WHERE id = @id";
                        selectCmd.Parameters.AddWithValue("@id", team_id);
                        using (var reader = selectCmd.ExecuteReader())
                        {
                            if (!reader.HasRows)
                            {
                                Selecter = true;
                            }
                        }
                        db.Close();
                    }
                    if (Selecter)
                    {
                        using (var db = new SqliteConnection("Data Source=bipki.db"))
                        {
                            //Use Set_Team.cs to set team_name
                            Set_Team set_Team2 = new Set_Team();
                            set_Team2.set_Text("Название команды");
                            set_Team2.ShowDialog();
                            //Get team_name from Set_Team.cs
                            string team_name = set_Team2.team_name;
                            db.Open();
                            var insertCmd = db.CreateCommand();
                            insertCmd.CommandText = "INSERT INTO teams (id, name) VALUES (@id, @name)";
                            insertCmd.Parameters.AddWithValue("@id", team_id);
                            insertCmd.Parameters.AddWithValue("@name", team_name);
                            insertCmd.ExecuteNonQuery();
                            db.Close();
                        }
                    }
                    //Add to teamStudent table student_id = id, team_id and name of selected file
                    using (var db = new SqliteConnection("Data Source=bipki.db"))
                    {
                        db.Open();
                        var insertCmd = db.CreateCommand();
                        insertCmd.CommandText = "INSERT INTO teamStudent (student_id, team_id, feedback) VALUES (@student_id, @team_id, @feedback)";
                        insertCmd.Parameters.AddWithValue("@student_id", Id);
                        insertCmd.Parameters.AddWithValue("@team_id", team_id);
                        insertCmd.Parameters.AddWithValue("@feedback", openFileDialog1.SafeFileName);
                        insertCmd.ExecuteNonQuery();
                        db.Close();
                    }

                }
            }
        }

        private void dataGridView1_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            
        }

        private void удалитьToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //Delete selected row if there at least one row
            if (dataGridView1.Rows.Count > 1)
            {
                //Delete from teamStudent table student_id = id, team_id and name of selected file
                using (var db = new SqliteConnection("Data Source=bipki.db"))
                {
                    db.Open();
                    var deleteCmd = db.CreateCommand();
                    deleteCmd.CommandText = "DELETE FROM teamStudent WHERE student_id = @student_id AND feedback = @feedback";
                    deleteCmd.Parameters.AddWithValue("@student_id", Id);
                    deleteCmd.Parameters.AddWithValue("@feedback", dataGridView1.Rows[Selected_row_index].Cells[0].Value.ToString());
                    deleteCmd.ExecuteNonQuery();
                    db.Close();
                }
                //Delete from Folder
                string path = System.IO.Path.Combine(Environment.CurrentDirectory, "Feedback");
                string path2 = System.IO.Path.Combine(path, dataGridView1.Rows[Selected_row_index].Cells[0].Value.ToString());
                System.IO.File.Delete(path2);
                //Delete from datagridview
                dataGridView1.Rows.RemoveAt(Selected_row_index);
            }
        }

        private void dataGridView1_CellMouseClick(object sender, DataGridViewCellMouseEventArgs e)
        {
            //If user click on cell with right mouse button
            if (e.Button == MouseButtons.Right)
            {
                //Select cell
                //If at least one row
                if (dataGridView1.Rows.Count > 1)
                {
                    //Select cell
                    dataGridView1.CurrentCell = dataGridView1.Rows[e.RowIndex].Cells[e.ColumnIndex];
                    //Get index of selected row
                    Selected_row_index = e.RowIndex;
                }
                //Show context menu
                contextMenuStrip1.Show(Cursor.Position);
            }
        }

        private void dataGridView2_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            //If clicked on empty cell in datagridview in first column open combobox with all existing subjects from db

        }

        private void radioButton1_CheckedChanged(object sender, EventArgs e)
        {
            //If checked set text of button2 to "Найти себя"
            if (radioButton1.Checked)
            {
                button2.Text = "Найти себя";
            }
        }

        private void radioButton2_CheckedChanged(object sender, EventArgs e)
        {
            //If checked set text of button2 to "Создать студента в базе данных"
            if (radioButton2.Checked)
            {
                button2.Text = "Создать студента в базе данных";
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
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
            switch (button2.Text)
            {
                case "Найти себя":
                    //If button2 text is "Найти себя"
                    FindStudent(textBox1.Text);
                    break;
                case "Создать студента в базе данных":
                    //If button2 text is "Создать студента в базе данных" create new student in db by opening Set_Student.cs
                    Student_Name = textBox1.Text;
                    Set_Student set_Student = new Set_Student();
                    set_Student.set_student_name(textBox1.Text);
                    set_Student.ShowDialog();
                    //Get student_id from Set_Student.cs
                    break;
                    
            }
        }

        private void FindStudent(string text)
        {
            //Find student in db
            //If student exists
            //Get student feedback from db
            //Get student subjects from db
            //Fill datagridview1 with student feedback
            //Fill datagridview2 with student subjects
            //Else
            //Show message "Студент не найден"
            string name = text;
            //open connection
            SqliteConnection db = new SqliteConnection("Data Source=bipki.db");
            db.Open();
            //create command
            SqliteCommand command = new SqliteCommand("SELECT id FROM Students WHERE Name = @name", db);
            command.Parameters.AddWithValue("@name", name);
            //execute command
            SqliteDataReader reader = command.ExecuteReader();
            //If student exists
            //Get from SubStu subject_id and mark
            //Then use subject_id to find name from subjects
            //Fill datagridview2 with subject name and mark
            //Fill datagridview1 with feedback
            if (reader.Read())
            {
                //Get student id
                Id = reader.GetInt32(0);
                //Get student feedback
                command = new SqliteCommand("SELECT feedback FROM teamStudent WHERE student_id = @id", db);
                command.Parameters.AddWithValue("@id", Id);
                reader = command.ExecuteReader();
                while (reader.Read())
                {
                    dataGridView1.Rows.Add(reader.GetString(0));
                }
                //Get student subjects
                command = new SqliteCommand("SELECT Subject_id, Mark FROM SubStu WHERE Student_id = @id", db);
                command.Parameters.AddWithValue("@id", Id);
                reader = command.ExecuteReader();
                while (reader.Read())
                {
                    //Get subject name
                    int subject_id = reader.GetInt32(0);
                    command = new SqliteCommand("SELECT Name FROM Subjects WHERE id = @id", db);
                    command.Parameters.AddWithValue("@id", subject_id);
                    SqliteDataReader reader2 = command.ExecuteReader();
                    reader2.Read();
                    string subject_name = reader2.GetString(0);
                    //Get mark
                    int mark = reader.GetInt32(1);
                    //Add subject name and mark to datagridview2
                    dataGridView2.Rows.Add(subject_name, mark);
                }
                //Show message "Студент найден"
                MessageBox.Show("Студент найден");
                button1.Enabled = true;
            }
            else
            {
                MessageBox.Show("Студент не найден");
            }
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
    }
}
