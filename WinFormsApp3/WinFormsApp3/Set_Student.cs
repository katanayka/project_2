using Microsoft.Data.Sqlite;

namespace WinFormsApp3
{
    public partial class Set_Student : Form
    {
        public void set_student_name(string name)
        {
            //Set student name
            textBox1.Text = name;
        }
        public Set_Student()
        {
            InitializeComponent();
            //Set name from faculties from DB to combobox2
            SqliteConnection db = new SqliteConnection("Data Source=bipki.db");
            db.Open();
            SqliteCommand cmd = new SqliteCommand("SELECT name FROM faculties", db);
            SqliteDataReader rdr = cmd.ExecuteReader();
            while (rdr.Read())
            {
                comboBox2.Items.Add(rdr.GetString(0));
            }
            db.Close();
            //resize combobox dropdown with values to fit all values
            comboBox2.DropDownHeight = 1;
            comboBox2.DropDownWidth = 1;
            foreach (string s in comboBox2.Items)
            {
                int width = TextRenderer.MeasureText(s, comboBox2.Font).Width;
                if (comboBox2.DropDownWidth < width)
                {
                    comboBox2.DropDownWidth = width;
                }
            }
            comboBox2.DropDownHeight = comboBox2.ItemHeight * 8;
        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            //Break if textboxes or comboboxes are empty
            if (textBox1.Text == "" || textBox2.Text == "" || comboBox1.Text == "" || comboBox2.Text == "")
            {
                MessageBox.Show("Заполните все поля!");
                return;
            }
            //Break if textbox2 has not only numbers, textbox1 has not only letters
            if (!textBox2.Text.All(char.IsDigit))
            {
                MessageBox.Show("Неверный формат данных!");
                return;
            }
            //Add student to DB
            //Get connection to DB
            SqliteConnection db = new SqliteConnection("Data Source=bipki.db");
            //Open connection
            db.Open();
            //Add student to DB
            SqliteCommand cmd = new SqliteCommand("INSERT INTO Students (id, name, course, faculty_id) VALUES (@id, @name,@course, @faculty_id)", db);
            cmd.Parameters.AddWithValue("@id", textBox2.Text);
            cmd.Parameters.AddWithValue("@name", textBox1.Text);
            cmd.Parameters.AddWithValue("@course", comboBox1.Text);
            //Get faculty_id by faculty_name from table
            int faculty_id = 0;
            SqliteCommand cmd2 = new SqliteCommand("SELECT id FROM faculties WHERE name = @name", db);
            cmd2.Parameters.AddWithValue("@name", comboBox2.Text);
            SqliteDataReader rdr = cmd2.ExecuteReader();
            while (rdr.Read())
            {
                faculty_id = rdr.GetInt32(0);
            }
            cmd.Parameters.AddWithValue("@faculty_id", faculty_id);
            cmd.ExecuteNonQuery();
            //Close connection
            cmd.Parameters.AddWithValue("@faculty_id", faculty_id);
            //If student with such id or name already exists in DB - show error
            
                cmd.ExecuteNonQuery();
                //Close connection
                db.Close();
                //Show message box
                MessageBox.Show("Студент добавлен");
                //Close form
                this.Close();
            
            

        }

        private void button2_Click(object sender, EventArgs e)
        {
            //Close form
            this.Close();
        }
    }
}
