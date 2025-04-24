import gpustat

def main():
    """
    Exibe o status das GPUs disponíveis.
    """
    stats = gpustat.new_query()
    print(stats)

if __name__ == "__main__":
    main()
