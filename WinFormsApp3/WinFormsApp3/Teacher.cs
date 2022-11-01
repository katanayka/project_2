using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Runtime.InteropServices;
using Excel = Microsoft.Office.Interop.Excel;
using Microsoft.Data.Sqlite;

namespace WinFormsApp3
{
    public partial class Teacher : Form
    {
        //cur folder + bipki.db
        string Default_Path_DB = System.IO.Path.GetDirectoryName(Application.ExecutablePath) + "\\bipki.db";
        public Teacher()
        {
            InitializeComponent();
            //If there no DB file, select by user file with DB
            if (!System.IO.File.Exists(Default_Path_DB))
            {
                //Create warning message
                MessageBox.Show("Файл базы данных не найден. Выберите файл базы данных.", "Внимание!", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                OpenFileDialog openFileDialog1 = new OpenFileDialog();
                openFileDialog1.Filter = "DB files (*.db)|*.db|All files (*.*)|*.*";
                openFileDialog1.FilterIndex = 1;
                openFileDialog1.RestoreDirectory = true;
                if (openFileDialog1.ShowDialog() == DialogResult.OK)
                {
                    Default_Path_DB = openFileDialog1.FileName;
                    //Copy selected file to application directory
                    System.IO.File.Copy(Default_Path_DB, System.IO.Path.GetDirectoryName(Application.ExecutablePath) + "\\bipki.db");
                }
                else
                {
                    Application.Exit();
                }
            }
        }
        private void button1_Click(object sender, EventArgs e)
        {
            //Open select file where can choose .csv, .xlsx, .sqlite
            OpenFileDialog openFileDialog1 = new OpenFileDialog();
            openFileDialog1.Filter = "CSV Files (*.csv)|*.csv|Excel Files (*.xlsx)|*.xlsx|SQLite Files (*.db)|*.db";
            openFileDialog1.Title = "Select a File";
            if (openFileDialog1.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                switch (openFileDialog1.FilterIndex)
                {
                    case 1:
                        //CSV
                        break;
                    case 2:
                        //Excel
                        /*
                        Read xlsx file (id,name,course,faculty_id,faculty_name)
                        Then add to DB
                        Check if there no such student in DB
                        If there is, then update
                        If there is no, then add
                        If there no such faculty, then add it
                        */
                        //Read xlsx file
                        string path = openFileDialog1.FileName;
                        Excel.Application xlApp = new Excel.Application();
                        Excel.Workbook xlWorkbook = xlApp.Workbooks.Open(path);
                        Excel._Worksheet xlWorksheet = xlWorkbook.Sheets[1];
                        Excel.Range xlRange = xlWorksheet.UsedRange;
                        int rowCount = xlRange.Rows.Count;
                        int colCount = xlRange.Columns.Count;
                        //Add to DB
                        //Check if there no such student in DB
                        //If there is, then update
                        //If there is no, then add
                        //If there no such faculty, then add it
                        //Create command using Microsoft.Data.Sqlite;
                        using (var connection = new SqliteConnection("Data Source=bipki.db"))
                        {
                            connection.Open();
                            //Open table with facilities and get all facilities
                            var selectFacilities = connection.CreateCommand();
                            selectFacilities.CommandText = "SELECT * FROM faculties";
                            var readerFacilities = selectFacilities.ExecuteReader();
                            //Create list with facilities
                            List<string> facilities = new List<string>();
                            while (readerFacilities.Read())
                            {
                                facilities.Add(readerFacilities.GetString(1));
                            }
                            //Open table with students and get all students
                            var selectStudents = connection.CreateCommand();
                            selectStudents.CommandText = "SELECT * FROM students";
                            var readerStudents = selectStudents.ExecuteReader();
                            //Create list with students
                            List<string> students = new List<string>();
                            while (readerStudents.Read())
                            {
                                students.Add(readerStudents.GetString(1));
                            }
                            //Create command for insert new student
                            var insertStudent = connection.CreateCommand();
                            insertStudent.CommandText = "INSERT INTO students (id, name, course, faculty_id) VALUES (@id, @name, @course, @faculty_id)";
                            insertStudent.Parameters.Add("@id", SqliteType.Integer);
                            insertStudent.Parameters.Add("@name", SqliteType.Text);
                            insertStudent.Parameters.Add("@course", SqliteType.Integer);
                            insertStudent.Parameters.Add("@faculty_id", SqliteType.Integer);
                            //Create command for update student
                            var updateStudent = connection.CreateCommand();
                            updateStudent.CommandText = "UPDATE students SET name = @name, course = @course, faculty_id = @faculty_id WHERE id = @id";
                            updateStudent.Parameters.Add("@id", SqliteType.Integer);
                            updateStudent.Parameters.Add("@name", SqliteType.Text);
                            updateStudent.Parameters.Add("@course", SqliteType.Integer);
                            updateStudent.Parameters.Add("@faculty_id", SqliteType.Integer);
                            //Create command for insert new faculty
                            var insertFaculty = connection.CreateCommand();
                            insertFaculty.CommandText = "INSERT INTO faculties (id, name) VALUES (@id, @name)";
                            insertFaculty.Parameters.Add("@id", SqliteType.Integer);
                            insertFaculty.Parameters.Add("@name", SqliteType.Text);
                            //Add new faculties if there no such faculty
                            //Create tuple of id and name of faculty from xlsx file
                            List<Tuple<int, string>> faculties = new List<Tuple<int, string>>();
                            for (int i = 2; i <= rowCount; i++)
                            {
                                faculties.Add(new Tuple<int, string>(Convert.ToInt32(xlRange.Cells[i, 4].Value2), xlRange.Cells[i, 5].Value2));
                            }
                            //Get only unique faculties
                            var uniqueFaculties = faculties.Distinct();
                            //Add new faculties if there no such faculty
                            foreach (var faculty in uniqueFaculties)
                            {
                                if (!facilities.Contains(faculty.Item2))
                                {
                                    insertFaculty.Parameters["@id"].Value = faculty.Item1;
                                    insertFaculty.Parameters["@name"].Value = faculty.Item2;
                                    insertFaculty.ExecuteNonQuery();
                                }
                            }
                            //Add new students if there no such student else update
                            for (int i = 2; i <= rowCount; i++)
                            {
                                if (!students.Contains(xlRange.Cells[i, 2].Value2.ToString()))
                                {
                                    insertStudent.Parameters["@id"].Value = xlRange.Cells[i, 1].Value2.ToString();
                                    insertStudent.Parameters["@name"].Value = xlRange.Cells[i, 2].Value2.ToString();
                                    insertStudent.Parameters["@course"].Value = xlRange.Cells[i, 3].Value2.ToString();
                                    insertStudent.Parameters["@faculty_id"].Value = xlRange.Cells[i, 4].Value2.ToString();
                                    insertStudent.ExecuteNonQuery();
                                }
                                else
                                {
                                    updateStudent.Parameters["@id"].Value = xlRange.Cells[i, 1].Value2.ToString();
                                    updateStudent.Parameters["@name"].Value = xlRange.Cells[i, 2].Value2.ToString();
                                    updateStudent.Parameters["@course"].Value = xlRange.Cells[i, 3].Value2.ToString();
                                    updateStudent.Parameters["@faculty_id"].Value = xlRange.Cells[i, 4].Value2.ToString();
                                    updateStudent.ExecuteNonQuery();
                                }
                            }
                            //Close connection
                            connection.Close();
                            //Close xlsx file
                            xlWorkbook.Close();
                            xlApp.Quit();
                            //Show message
                            MessageBox.Show("Файл успешно загружен");
                        }




                        break;
                    case 3:
                        //SQLite
                        break;
                }
            }

        }

        private void Teacher_Load(object sender, EventArgs e)
        {

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
