#include <stdio.h>
#include <stdlib.h>

//Function prototypes
void asciiart(void);
void get_payoffs(float* matrix);



int main(void)
{
	asciiart();
	float payoffs[8]; //Generate empty payoff matrix
	get_payoffs(payoffs); //Call function to fill payoff matrix
	
	printf("\nOverview of payoffs:\n"); //Print overview table of payoff values
	for (int i = 0; i < 8; i++)
	{
		if (i == 0)
		{
			printf("\nRow player\n");
			printf("------------\n");
		}
		else if (i == 4)
		{
			printf("\nColumn player\n");
			printf("------------\n");
		}
		printf("%c: %f\n", (char) i + 65, payoffs[i]);
	}
	
	return 0;
}


void asciiart(void)
{
	int number_of_lines = 11;
	char *lines[number_of_lines];
	lines[0] = "\n";
	lines[1] = "               L           R     \n";
	lines[2] = "\n";
	lines[3] = "   U            E           F        p\n";
	lines[4] = "               A           B          \n";
	lines[5] = "\n";
	lines[6] = "   D            G           H        (1-p)\n";
	lines[7] = "               C           D              \n";
	lines[8] = "\n";
	lines[9] = "               q          (1-q)      \n";
	lines[10] = "\n";

	for (int i = 0; i < number_of_lines; i++)
		printf("%s\n", lines[i]);
}

void get_payoffs(float* matrix) //This function fills the payoff matrix
{
	
	//Collect manual entry of payoffs for row player
	printf("A  B\n");
	printf("C  D\n");
	printf("Please enter payoffs for row player A, B, C, D, separated by commas: ");
	scanf("%f, %f, %f, %f", &matrix[0], &matrix[1], &matrix[2], &matrix[3]);
	
	//Ask if game is fixed sum (ask until answer is y, Y, n or N)
	char fixed_sum;
	while ( ((int) fixed_sum != 89) && ( (int) fixed_sum != 121) && ( (int) fixed_sum != 78) && ( (int) fixed_sum != 110) )
	{
	printf("\nFixed sum (y/n)? ");
	scanf(" %c", &fixed_sum);
	}
	
	if ( ( (int) fixed_sum == 89) || ( (int) fixed_sum == 121) )
	{	//If fixed-sum, automatically calculate column player payoffs as difference between sum and row player payoffs
		float sum;
		printf("What is that sum? ");
		scanf("%f", &sum);
		for (int i = 4; i < 8; i++)
			matrix[i] = sum - matrix[i - 4];
	}	
	else if ( ( (int) fixed_sum == 78) || ( (int) fixed_sum == 110) )	
	{	//If not fixed sum, collect manual entry of column player payoffs
		printf("E  F\n");
		printf("G  H\n");
		printf("Please enter payoffs for column player E, F, G, H, separated by commas: ");
		scanf("%f, %f, %f, %f", &matrix[4], &matrix[5], &matrix[6], &matrix[7]);
	}
	
	
	return;
}
