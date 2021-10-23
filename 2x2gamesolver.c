#include <stdio.h>
#include <stdlib.h>

//Function prototypes
void asciiart(void);
void get_payoffs(float matrix[2][2][2]);
void print_overview(float matrix[2][2][2], int p);
int dominancechecker(float checked1, float alternative1, float checked2, float alternative2);
int flip (int x);


int main(void)
{
	asciiart();
	float payoffs[2][2][2]; //Generate empty payoff matrix
	get_payoffs(payoffs); //Call function to fill payoff matrix
	
	//Print overview table of payoff values
	printf("\n\nOverview over collected payoffs:\n\n");
    print_overview(payoffs, 0);
    printf("\nColumn player:\n------------\n");
    print_overview(payoffs, 1);
	
	
	int *dominance_results = malloc(sizeof(int) * 4); //allocate memory for four dominance variables:
	//A dominance variable is 2 if corresponding pure strategy is strictly dominant,
	//1 if weakly dominant,
	//0 otherwise
	
    //Running dominance checks for row player
    int i = 0;
    while (i < 2)
    {
        dominance_results[i] = dominancechecker(payoffs[0][i][0], payoffs[0][flip(i)][0], payoffs[0][i][1], payoffs[0][flip(i)][1]);
        i++;
    }
    
    //Running dominance checks for column player
    i = 0;
    while (i < 2)
    {
        dominance_results[i + 2] = dominancechecker(payoffs[1][0][i], payoffs[1][0][flip(i)], payoffs[1][1][i], payoffs[1][1][flip(i)]);
        i++;
    }
	
	char* pure_strategies[] = {"Up", "Down", "Left", "Right"}; //Array that assigns each numerical code for a pure strategy the name of that strategy
	
	//Print results of dominance check
	printf("\nResults of dominance check:\n\n");
    int* dominance_sum = malloc(sizeof(int)); //dominance_sum is used to keep track if any dominance exists (0 if there is none)
    if (dominance_sum == NULL)
        return 1;
    *dominance_sum = 0;
    i = 0;
	while (i < 4)
	{
		if (dominance_results[i] == 2)
        {
			printf("%s is strictly dominant\n", pure_strategies[i]);
            (*dominance_sum)++;
        }
		else if (dominance_results[i] == 1)
        {
			printf("%s is weakly dominant\n", pure_strategies[i]);
            (*dominance_sum)++;
        }
        i++;
	}
    if (*dominance_sum == 0)
        printf("No dominance detected\n");
	
    printf("\nPure strategy Nash equilibria:\n");
    
    int nash[2][2]; //Array that holds binary variables for pure strategies
    //Value to be 1 if that pure strategy is a Nash equilibrium, 0 otherwise
    int nashsum = 0; //sum of the Nash array
    for (int j1 = 0; j1 < 2; j1++)
    {
        for (int k1 = 0; k1 < 2; k1++)
        {
            if ((payoffs[0][k1][j1] >= payoffs[0][flip(k1)][j1]) && (payoffs[1][k1][j1] >= payoffs[1][k1][flip(j1)]))
                {
                    nash[k1][j1] = 1;
                    nashsum++;
                }
            else
                nash[k1][j1] = 0;
        }
    }
    
    if (nashsum == 0)
            printf("No pure strategy Nash equilibria detected.\n");
    else
    {
        for (int j2 = 0; j2 < 2; j2++)
        {
            for (int k2 = 0; k2 < 2; k2++)
            {
                if (nash[k2][j2] == 1)
                    printf("%s, %s\n", pure_strategies[k2], pure_strategies[j2 + 2]);
            }
        }
    }
    
    //Calculate mixed strategy Nash equilibria
    float numerator_p, numerator_q;
    float denominator_p, denominator_q;
    numerator_q = payoffs[0][1][1] - payoffs[0][0][1];
    denominator_q = payoffs[0][0][0] - payoffs[0][0][1] - payoffs[0][1][0] + payoffs[0][1][1];
    numerator_p = payoffs[1][1][1] - payoffs[1][1][0];
    denominator_p = payoffs[1][0][0] - payoffs[1][1][0] - payoffs[1][0][1] + payoffs[1][1][1];
    float p = numerator_p / denominator_p;
    float q = numerator_q / denominator_q;
    
    if ((0 < p) && (0 < q ) && ( p < 1) && (q < 1))
        printf("\nResults of mixed strategy analysis:\np: %f\nq: %f", p, q);
    else
        printf("\nNo mixed strategy Nash equlibria\n");
    
    //End of main function
    
    free(dominance_results);
    free(dominance_sum);
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

void get_payoffs(float matrix[2][2][2]) //This function fills the payoff matrix
{
	
	//Collect manual entry of payoffs for row player
	printf("A  B\n");
	printf("C  D\n");
	printf("Please enter payoffs for row player A, B, C, D, separated by commas: ");
	scanf("%f, %f, %f, %f", &matrix[0][0][0], &matrix[0][0][1], &matrix[0][1][0], &matrix[0][1][1]);
	
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
		for (int i = 0; i < 2; i++)
        {
            for (int j = 0; j < 2; j++)
                matrix[1][i][j] = sum - matrix[0][i][j];
        }
	}	
	else if ( ( (int) fixed_sum == 78) || ( (int) fixed_sum == 110) )	
	{	//If not fixed sum, collect manual entry of column player payoffs
		printf("E  F\n");
		printf("G  H\n");
		printf("Please enter payoffs for column player E, F, G, H, separated by commas: ");
		scanf("%f, %f, %f, %f", &matrix[1][0][0], &matrix[1][0][1], &matrix[1][1][0], &matrix[1][1][1]);
	}
	
	
	return;
}

void print_overview(float matrix[2][2][2], int p)
{
    for (int x = 0; x < 2; x++)
    {
        for (int y = 0; y < 2; y++)
        {
            printf("%f       ", matrix[p][x][y]);
            if (y == 1)
                printf("\n");
        }
    }
}

int dominancechecker(float checked1, float alternative1, float checked2, float alternative2) //Checks a given strategy for strict or weak dominance over its alternative
{
	if ((checked1 > alternative1) && (checked2 > alternative2))
		return 2;
	else if ((checked1 >= alternative1) && (checked2 >= alternative2))
		return 1;
	else
		return 0;
}

int flip(int x) //Turns an index number of 0 or 1 into its opposite
{
    return ((x + 1) % 2);
}
