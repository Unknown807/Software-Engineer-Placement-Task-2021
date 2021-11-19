# Software-Engineer-Placement-Task-2021
## Description

This is a program that works with an API that was provided to me as part of my placement task. The program does simple visualisation of cost/consumption data of (from the looks of it) various cloud-related resources and applications (which can make use of multiple resources), along with some min/max calculations.

## Libraries Used

- tkinter
- pickle
- matplotlib
- requests
- urllib
- Pmw

## How It Works

![](/repo_imgs/img1.png)

when you open the program you will be greeted with the screen above

![](/repo_imgs/img2.png)

Above, I use the API to select resources and then choose 'Storage' with a unit of measurement being 100 GB (provided by the API). Now, because the differences between the data are very small and close together, I log the y axis in order to better represent how significant each bar column is. Although the y axis is now in standard form, if you hover your mouse over the bars you will still see the original values.

![](/repo_imgs/img3.png)

Now by selecting applications instead, followed by the 'index-Consultant-blue' application I clicked the 'min cost/consumption' button, to get the lowest consumption of all the resources that said application uses. In this case its the Advanced Threat Protecton resource
