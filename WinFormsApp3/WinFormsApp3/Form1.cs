namespace WinFormsApp3
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            //Center text label
            label1.Left = (this.ClientSize.Width - label1.Width) / 2;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            //Open Student form
            Student student = new Student();
            student.Show();
            this.Hide();
            student.FormClosed += (s, args) => this.Close();
            
        }

        private void button2_Click(object sender, EventArgs e)
        {
            //Open Teacher Form
            Teacher f3 = new Teacher();
            f3.Show();
            this.Hide();
            f3.FormClosed += (s, args) => this.Close();
        }

        private void button3_Click(object sender, EventArgs e)
        {
            //Enter password in new opened form and open DB form if password is correct
            Password f4 = new Password();
            f4.ShowDialog();
            if (f4.DialogResult == DialogResult.OK)
            {
                DB f5 = new DB();
                f5.Show();
                this.Hide();
                f5.FormClosed += (s, args) => this.Close();
            }
        }
    }
}