O objetivo principal deste documento é manter uma ordenação de como os conceitos vão sendo desenvolvidos e documentar os avanços que vão sendo obtidos  
  
Como os chats nas IAs tem uma limitação de tamanho, ou por tokens ou por conceitos apresentados, regularmente é preciso fazer a troca de chat e o primeiro prompt é fundamental para que aquele chat se desenvolva bem: é preciso instrui-lo com tudo aquilo que foi desenvolvido, tanto quanto a forma e o papel de cada um se relacionar, como quanto ao projeto em si.  
  
O protocolo de relacionamento está aqui [[protocolo-de-interacao]]

O desenvolvimento está sendo feito através de notebooks, 
1. [a-recepcao - raw](https://github.com/WRMELO/INFRAESTRUTURA/blob/main/notebooks/a-recepcao-raw.ipynb)  que pega os arquivos que estão no My Drive (fonte primária dos arquivos) e os copia em um bucket MinIO [recepcao-raw](pipeline-projeto.md#Infresturura) . Faz a auditoria através de uma tabela [[Pasted image 20250529074441.png|reception_audit]].
2. [b-starage-movimentacao-unico](https://github.com/WRMELO/INFRAESTRUTURA/blob/main/notebooks/b-storage-movimentacao-unico.ipynb), que tem seu processo descrito [aqui](pipeline-notebook-b). As tabelas que garantem unicidade de [[Pasted image 20250529080549.png|projetos]] e de [[Pasted image 20250529080558.png|arquivos]].


