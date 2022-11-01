using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WinFormsApp3
{
    public partial class Set_Team : Form
    {
        public int team_id = -1;
        public string team_name = "";
        public Set_Team()
        {
            InitializeComponent();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            //Return dialog result Cancel
            this.DialogResult = DialogResult.Cancel;
            this.Close();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            //if text is int
            //team_id = Convert.ToInt32(textBox1.Text);
            //if text is string
            //team_name = textBox1.Text;

            //get type of text
            if (int.TryParse(textBox1.Text, out team_id))
            {
                //if text is int
                team_id = Convert.ToInt32(textBox1.Text);
                this.DialogResult = DialogResult.OK;
                this.Close();
            }
            else
            {
                //if text is string
                team_name = textBox1.Text;
                this.DialogResult = DialogResult.OK;
                this.Close();
            }
        }
        public void set_Text(string text)
        {
            //Set label text
            label1.Text = text;
        }
    }
}
