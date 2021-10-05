#include <stdio.h>
#include <stdlib.h>

//Function prototypes
void asciiart(void);
void get_payoffs(float* matrix);
int dominancechecker(float* pomatrix, int c1, int c2, int c3, int c4);


int main(void)
{
	asciiart();
	float payoffs[8]; //Generate empty payoff matrix
	get_payoffs(payoffs); //Call function to fill payoff matrix
	
	//Print overview table of payoff values
	printf("\n\nOverview over collected payoffs:\n\n");
	for (int x = 0; x < 8; x++)
	{
		if (x == 0)
			printf("\nRow player:\n------------\n");
		if (x == 4)
			printf("\nColumn player:\n------------\n");
		printf("%f		", payoffs[x]);
		if (x % 2 == 1)
			printf("\n");
	}
	
	int dominance_array[4]; //Generate array of dominance variables
	//dominance variable is 2 if corresponding pure strategy is strictly dominant,
	//1 if weakly dominant,
	//0 otherwise
	
	
	dominance_array[0] = dominancechecker(payoffs, 0, 2, 1, 3); //Dominance variable for UP
	dominance_array[1] = dominancechecker(payoffs, 2, 0, 3, 1); //Dominance variable for DOWN
	dominance_array[2] = dominancechecker(payoffs, 4, 5, 6, 7); //Dominance variable for LEFT
	dominance_array[3] = dominancechecker(payoffs, 5, 4, 7, 6); //Dominance variable for RIGHT
	
	char* pure_strategies[] = {"Up", "Down", "Left", "Right"}; //Array that assigns each numerical code for a pure strategy the name of that strategy
	
	//Print results of dominance check
	printf("\nResults of dominance check:\n\n");
	for (int j = 0; j < 4; j++)
	{
		if (dominance_array[j] == 2)
			printf("%s is strictly dominant\n", pure_strategies[j]);
		else if (dominance_array[j] == 1)
			printf("%s is weakly dominant\n", pure_strategies[j]);
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

int dominancechecker(float* pomatrix, int c1, int c2, int c3, int c4) //Checks a given strategy for strict or weak dominance
{
	if ( (pomatrix[c1] > pomatrix[c2]) && (pomatrix[c3] > pomatrix[c4]) )
		return 2;
	else if ( (pomatrix[c1] >= pomatrix[c2]) && (pomatrix[c3] >= pomatrix[c4]) )
		return 1;
	else
		return 0;
}

